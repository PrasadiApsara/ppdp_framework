import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-build-model',
  templateUrl: './build-model.component.html',
  styleUrls: ['./build-model.component.css']
})
export class BuildModelComponent implements OnInit {

  constructor(private dataService: DataService) { }

  modelAccuracy: number;
  modelType: string;
  tagCategories: string;
  showSpinner = false;
  isLoaded = false;

  ngOnInit() {
  }

  onTrainButtonClicked() {
    this.showSpinner = true;
    this.dataService.getData().subscribe(
      (res: any) => {
        this.modelAccuracy = res.accuracy;
        this.modelType = 'Decision tree based tagger';
        this.tagCategories = 'SA|QIAGE|QIJOB|QIGENDER|QIREGION|QIRACE';
        this.showSpinner = false;
        this.isLoaded = true;
      }
    );
  }

}
