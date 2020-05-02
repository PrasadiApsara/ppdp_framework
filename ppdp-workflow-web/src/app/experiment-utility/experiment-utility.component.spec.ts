import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentUtilityComponent } from './experiment-utility.component';

describe('ExperimentUtilityComponent', () => {
  let component: ExperimentUtilityComponent;
  let fixture: ComponentFixture<ExperimentUtilityComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExperimentUtilityComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExperimentUtilityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
