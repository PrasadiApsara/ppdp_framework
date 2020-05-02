import { Component, OnInit, Pipe, PipeTransform, } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-experiment-anonymize',
  templateUrl: './experiment-anonymize.component.html',
  styleUrls: ['./experiment-anonymize.component.scss']
})
export class ExperimentAnonymizeComponent implements OnInit {

  titleGenderDisc = 'Discernability - Gender';
  titleAgeDisc = 'Discernability - Age';
  titleJobDisc = 'Discernability - Job';
  titleRegionDisc = 'Discernability - Region';
  titleReligionDisc = 'Discernability - Religion';
  titleLanguageDisc = 'Discernability - Language';
  titleMaritalDisc = 'Discernability - Marital Status';
  titleGenderLoss = 'Loss - Gender';
  titleAgeLoss = 'Loss - Age';
  titleJobLoss = 'Loss - Job';
  titleRegionLoss = 'Loss - Region';
  titleReligionLoss = 'Loss - Religion';
  titleLanguageLoss = 'Loss - Language';
  titleMaritalLoss = 'Loss - Marital Status';
  type = 'PieChart';
  columnNames = ['Sanitized Quasi Identifier Value', 'Discernability'];
  columnNamesLoss = ['Quasi Identifier Value', 'Loss'];
  dataGenderDisc = [];
  dataAgeDisc = [];
  dataJobDisc = [];
  dataRegionDisc = [];
  dataReligionDisc = [];
  dataLanguageDisc = [];
  dataMaritalDisc = [];
  dataGenderLoss = [];
  dataAgeLoss = [];
  dataJobLoss = [];
  dataRegionLoss = [];
  dataReligionLoss = [];
  dataLanguageLoss = [];
  dataMaritalLoss = [];
  options = {
    pieSliceText: 'value'
  };

  constructor(private dataService: DataService) { }

  taggedSentences: string[] = [];
  sanitizedSentences: string[] = [];
  sanitizationCount: string;
  sanitizationPercentage: string;
  showSpinner = false;
  isAnonymizationPanelExpanded = false;

  ngOnInit() {
  }

  onTrainButtonClicked() {
    this.showSpinner = true;
    this.dataService.tryExperiment().subscribe(
      (res: any) => {
        this.taggedSentences = res.tagged;
        this.sanitizedSentences = res.sanitized;
        this.sanitizationCount = res.count;
        this.sanitizationPercentage = res.percentage;
        this.showSpinner = false;
        this.isAnonymizationPanelExpanded = true;
      }
    );
  }

 public checkSentence(sentence: string) {
    const arr = sentence.split(' ');
    let formattedString = '';
    arr.forEach(
      (a) => {
        if (a.includes('/QIREGION')) {
          a = a.replace('QIREGION', '<span style="background-color:#fff;border-radius: 4px;">QIREGION</span>');
          a = a.replace(a, '<span style="background-color:#a6e22d; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        if (a.includes('/SA')) {
          a = a.replace('SA', '<span style="background-color:#fff;border-radius: 4px;">SA</span>');
          a = a.replace(a, '<span style="background-color:#ef60b4; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        if (a.includes('QIAGE')) {
          a = a.replace('QIAGE', '<span style="background-color:#fff;border-radius: 4px;">QIAGE</span>');
          a = a.replace(a, '<span style="background-color:#a99dfb; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        if (a.includes('/QIGENDER')) {
          a = a.replace('QIGENDER', '<span style="background-color:#fff;border-radius: 4px;">QIGENDER</span>');
          a = a.replace(a, '<span style="background-color:#2fbbab; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        if (a.includes('/QIJOB')) {
          a = a.replace('QIJOB', '<span style="background-color:#fff;border-radius: 4px;">QIJOB</span>');
          a = a.replace(a, '<span style="background-color:#fd9720; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        if (a.includes('/QIRELIGION')) {
          a = a.replace('QIRELIGION', '<span style="background-color:#fff;border-radius: 4px;">QIRELIGION</span>');
          a = a.replace(a, '<span style="background-color:#AFFF33; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        if (a.includes('/QILANG')) {
          a = a.replace('QILANG', '<span style="background-color:#fff;border-radius: 4px;">QILANG</span>');
          a = a.replace(a, '<span style="background-color:#33D5FF; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        if (a.includes('/QIMARITAL')) {
          a = a.replace('QIMARITAL', '<span style="background-color:#fff;border-radius: 4px;">QIMARITAL</span>');
          a = a.replace(a, '<span style="background-color:#FF339F; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        if (a.includes('/DI')) {
          a = a.replace('DI', '<span style="background-color:#fff;border-radius: 4px;">DI</span>');
          a = a.replace(a, '<span style="background-color:#bbb; padding:5px;border-radius: 8px;">' + a + '</span>');
        }
        formattedString += a + ' ';
      });
    return formattedString;
  }

  evaluate() {
    this.dataService.evaluatePseudoanonymized().subscribe(
      (res: any) => {
        this.dataGenderDisc = res.gender;
        this.dataAgeDisc = res.age;
        this.dataJobDisc = res.job;
        this.dataRegionDisc = res.region;
        this.dataReligionDisc = res.religion;
        this.dataLanguageDisc = res.language;
        this.dataMaritalDisc = res.marital;
        this.dataGenderLoss = res.genderLoss;
        this.dataAgeLoss = res.ageLoss;
        this.dataJobLoss = res.jobloss;
        this.dataRegionLoss = res.regionloss;
        this.dataReligionLoss = res.religionLoss;
        this.dataLanguageLoss = res.languageloss;
        this.dataMaritalLoss = res.maritalloss;
      }
    );
  }

}
