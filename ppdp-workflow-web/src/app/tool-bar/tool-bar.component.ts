import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-tool-bar',
  templateUrl: './tool-bar.component.html',
  styleUrls: ['./tool-bar.component.scss']
})
export class ToolBarComponent implements OnInit {
  @Input()
  sidenav: any;
  constructor() { }

  ngOnInit() {
  }

  
}
