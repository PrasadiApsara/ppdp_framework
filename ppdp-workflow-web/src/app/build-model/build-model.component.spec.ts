import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BuildModelComponent } from './build-model.component';

describe('BuildModelComponent', () => {
  let component: BuildModelComponent;
  let fixture: ComponentFixture<BuildModelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BuildModelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BuildModelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
