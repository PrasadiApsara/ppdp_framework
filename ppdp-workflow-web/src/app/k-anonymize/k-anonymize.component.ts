import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

export interface PeriodicElement {
  age: number;
  gender: string;
  job: string;
  region: string;
  religion: string;
  language: string;
  marital: string;
  sa: string;
  count: number;
  rows: string;
}


@Component({
  selector: 'app-k-anonymize',
  templateUrl: './k-anonymize.component.html',
  styleUrls: ['./k-anonymize.component.css']
})

export class KAnonymizeComponent implements OnInit {
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

  keyword = '';
  showSpinner = false;
  isLoaded = false;
  displayedColumns: string[] = ['age', 'gender', 'job', 'region', 'religion', 'language', 'marital', 'sa', 'count', 'rows'];
  dataSource: PeriodicElement[] = [];
  sanitizedSentences: string[] = [];
  sanitizationCount: string;
  sanitizationPercentage: string;
  isAnonymizationPanelExpanded = false;


  ngOnInit() {
  }

  exportAndKanonymize() {
    this.showSpinner = true;
    this.dataService.exportAndKanonymize(this.keyword).subscribe(
      (res: any) => {
        this.dataSource = JSON.parse(res.exportedtweet);
        this.sanitizedSentences = res.sanitized;
        this.sanitizationCount = res.count;
        this.sanitizationPercentage = res.percentage;
        this.showSpinner = false;
        this.isLoaded = true;
        this.isAnonymizationPanelExpanded = true;
      }
    );
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

  clearSentence() {
    this.keyword = '';
    this.dataGenderDisc = [];
    this.dataAgeDisc = [];
    this.dataJobDisc = [];
    this.dataRegionDisc = [];
    this.dataGenderLoss = [];
    this.dataAgeLoss = [];
    this.dataJobLoss = [];
    this.dataRegionLoss = [];
    this.dataSource = [];
    this.isLoaded = false;
    this.sanitizedSentences = [];
    this.sanitizationCount = '';
    this.sanitizationPercentage = '';
  }

}
