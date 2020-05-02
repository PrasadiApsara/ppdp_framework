import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-pseudoanonymize',
  templateUrl: './pseudoanonymize.component.html',
  styleUrls: ['./pseudoanonymize.component.css']
})
export class PseudoanonymizeComponent implements OnInit {

  constructor(private dataService: DataService) { }

  sentence = '';
  taggedSentence = '';
  anonymizedSentence = '';
  showSpinner = false;

  ngOnInit() {
  //  this.sentence = 'TEST';
  }

  pseudoanonymize() {
    this.showSpinner = true;
    this.dataService.psedoanonymize(this.sentence).subscribe(
      (res: any) => {
        this.taggedSentence = res.tags;
        this.anonymizedSentence = res.sanitizations;
        this.showSpinner = false;
      }
    );
  }
  clearSentence() {
    this.sentence = '';
    this.taggedSentence = '';
    this.anonymizedSentence = '';
  }
  public checkSentence() {
    const arr = this.taggedSentence.split(' ');
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
}
