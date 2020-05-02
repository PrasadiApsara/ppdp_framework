import pandas as pd
from pymongo import MongoClient

class KAnonymizer:
    names = (
        'age',
        'region', #Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
        'gender', # "weight" of that person in the dataset (i.e. how many people does that person represent) -> https://www.kansascityfed.org/research/datamuseum/cps/coreinfo/keyconcepts/weights
        'job',
        'religion',
        'language',
        'marital',
        'sa',
        'rowno'
        )

        # some fields are categorical and will require special treatment
    categorical = set((
            'region',
            'gender',
            'job',
            'religion',
            'language',
            'marital',
            'sa',
        ))
    def configure(self):
        conn = MongoClient() 
        # database 
        db = conn.ppdp 
        # Created or Switched to collection names: my_gfg_collection 
        collection = db.unsanitizeddata 
        df =  pd.DataFrame(list(collection.find({}, {'_id':0})))

        for name in self.categorical:
            df[name] = df[name].astype('category')
        return df

    def get_spans(self, df, partition, scale=None):
        """
        :param        df: the dataframe for which to calculate the spans
        :param partition: the partition for which to calculate the spans
        :param     scale: if given, the spans of each column will be divided
                          by the value in `scale` for that column
        :        returns: The spans of all columns in the partition
        """
        spans = {}
        for column in df.columns:
            if column in self.categorical:
                processed = pd.Series()
                for index, value in df[column][partition].items():
                    processed.set_value(index, self.remov_punct(str(value)))
                span = len(processed.unique())
            else:
                processed = pd.Series()
                for index, value in df[column][partition].items():
                    processed.set_value(index, self.remov_punct(str(value)))
                    if(processed.max().isnumeric()):
                        max = float(processed.max())
                    else: 
                        max = 0;
                    if(processed.min().isnumeric()):
                        min = float(processed.min())
                    else:
                        min = 0;
                print(max)
                print(min)
                span = max-min
            if scale is not None:
                if(scale[column] is 0):
                    scale[column] = 1
                span = span/scale[column]
            spans[column] = span
        return spans

    def split(self, df, partition, column):
        """
        :param        df: The dataframe to split
        :param partition: The partition to split
        :param    column: The column along which to split
        :        returns: A tuple containing a split of the original partition
        """
        dfp = df[column][partition]
        if column in self.categorical:
            processed = pd.Series()
            for index, value in dfp.items():
                processed.set_value(index, self.remov_punct(str(value)))
            values = processed.unique()
            lv = set(values[:len(values)//2])
            rv = set(values[len(values)//2:])
            return processed.index[processed.isin(lv)], processed.index[processed.isin(rv)]
        else:
            processed = pd.Series()
            for index, value in dfp.items():
                if(self.remov_punct(str(value)).isnumeric()):
                    processed.set_value(index, float(self.remov_punct(str(value))))
                else:
                    processed.set_value(index, 0)
            median = processed.median()
            print(median)
            dfl = processed.index[processed < median]
            dfr = processed.index[processed >= median]
            return (dfl, dfr)

    def is_k_anonymous(self, df, partition, sensitive_column, k=4):
        """
        :param               df: The dataframe on which to check the partition.
        :param        partition: The partition of the dataframe to check.
        :param sensitive_column: The name of the sensitive column
        :param                k: The desired k
        :returns               : True if the partition is valid according to our k-anonymity criteria, False otherwise.
        """
        if len(partition) < k:
            return False
        return True

    def partition_dataset(self, df, feature_columns, sensitive_column, scale, is_valid):
        """
        :param               df: The dataframe to be partitioned.
        :param  feature_columns: A list of column names along which to partition the dataset.
        :param sensitive_column: The name of the sensitive column (to be passed on to the `is_valid` function)
        :param            scale: The column spans as generated before.
        :param         is_valid: A function that takes a dataframe and a partition and returns True if the partition is valid.
        :returns               : A list of valid partitions that cover the entire dataframe.
        """
        finished_partitions = []
        partitions = [df.index]
        while partitions:
            partition = partitions.pop(0)
            spans = self.get_spans(df[feature_columns], partition, scale)
            for column, span in sorted(spans.items(), key=lambda x:-x[1]):
                lp, rp = self.split(df, partition, column)
                if not is_valid(df, lp, sensitive_column) or not is_valid(df, rp, sensitive_column):
                    continue
                partitions.extend((lp, rp))
                break
            else:
                finished_partitions.append(partition)
        return finished_partitions

    def agg_categorical_column(self, series):
        processed = pd.Series()
        for index, value in series.items():
            processed.set_value(index, self.remov_punct(str(value)))
        return [','.join(set(processed))]

    def agg_numerical_column(self, series):
        processed = pd.Series()
        for index, value in series.items():
            if(self.remov_punct(str(value)).isnumeric()):
                processed.set_value(index, float(self.remov_punct(str(value))))
            else:
                processed.set_value(index, 0)
        print(processed)
        return [processed.mean()]

    def remov_punct(self, withpunct):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        without_punct = ""
        char = 'nan'
        for char in withpunct:
            if char not in punctuations:
                without_punct = without_punct + char
        return(without_punct)

    def build_anonymized_dataset(self, df, partitions, feature_columns, sensitive_column, max_partitions=None):
        df['rowno'] = df['rowno'].apply(str)
        for index, row in df.iterrows():
            row["sa"] = self.remov_punct(row["sa"]).lower()
        aggregations = {}
        for column in feature_columns:
            if column in self.categorical:
                aggregations[column] = self.agg_categorical_column
            else:
                aggregations[column] = self.agg_numerical_column
        rows = []
        for i, partition in enumerate(partitions):
            if i % 100 == 1:
                print("Finished {} partitions...".format(i))
            if max_partitions is not None and i > max_partitions:
                break
            grouped_columns = df.loc[partition].agg(aggregations, squeeze=False)
            sensitive_counts = df.loc[partition].groupby(sensitive_column).agg({sensitive_column : 'count', 'rowno': ','.join})
            values = grouped_columns.iloc[0].to_dict()
            for val in sensitive_counts.iterrows():
                sensitive_value = self.remov_punct(val[0])
                count = val[1]['sa']
                rowcount = val[1]['rowno']
                if count == 0:
                    continue
                values.update({
                    sensitive_column : sensitive_value,
                    'count' : count,
                    'rows' : rowcount
                })
                rows.append(values.copy())
        return pd.DataFrame(rows)

    def execute_anonymization(self):
        df = self.configure()
        feature_columns = ['age', 'region', 'gender', 'job', 'religion', 'language', 'marital']
        sensitive_column = 'sa'
        full_spans = self.get_spans(df, df.index)
        finished_partitions = self.partition_dataset(df, feature_columns, sensitive_column, full_spans, self.is_k_anonymous)
        dfn = self.build_anonymized_dataset(df, finished_partitions, feature_columns, sensitive_column)
        dfn.sort_values(feature_columns+[sensitive_column])
        print(dfn)
        return dfn
