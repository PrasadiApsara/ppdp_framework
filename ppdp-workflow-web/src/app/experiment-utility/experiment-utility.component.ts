import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-experiment-utility',
  templateUrl: './experiment-utility.component.html',
  styleUrls: ['./experiment-utility.component.scss']
})
export class ExperimentUtilityComponent implements OnInit {

  constructor(private dataService: DataService) { }
  modelAccuracy: string;
  modelAccuracySimpleAnonymization: string;
  showSpinnerNormal = false;
  showSpinnerSimple = false;

  ngOnInit() {
  }
  onTrainButtonClicked() {
    this.showSpinnerNormal = true;
    this.dataService.getUtilityTest().subscribe(
      (res: any) => {
        this.modelAccuracy = res.accuracy;
        this.showSpinnerNormal = false;
      }
    );
  }

  onTrainButtonAnonymizedClicked() {
    this.showSpinnerSimple = true;
    this.dataService.getUtilityTestAnonymized().subscribe(
      (res: any) => {
        this.modelAccuracySimpleAnonymization = res.accuracy;
        this.showSpinnerSimple = false;
      }
    );
  }

}
