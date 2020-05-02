import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentKanonymizeComponent } from './experiment-kanonymize.component';

describe('ExperimentKanonymizeComponent', () => {
  let component: ExperimentKanonymizeComponent;
  let fixture: ComponentFixture<ExperimentKanonymizeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExperimentKanonymizeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExperimentKanonymizeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
