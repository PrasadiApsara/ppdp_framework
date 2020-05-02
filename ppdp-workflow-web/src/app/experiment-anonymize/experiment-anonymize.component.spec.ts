import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentAnonymizeComponent } from './experiment-anonymize.component';

describe('ExperimentAnonymizeComponent', () => {
  let component: ExperimentAnonymizeComponent;
  let fixture: ComponentFixture<ExperimentAnonymizeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExperimentAnonymizeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExperimentAnonymizeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
