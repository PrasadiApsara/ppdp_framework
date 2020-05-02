import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PseudoanonymizeComponent } from './pseudoanonymize.component';

describe('PseudoanonymizeComponent', () => {
  let component: PseudoanonymizeComponent;
  let fixture: ComponentFixture<PseudoanonymizeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PseudoanonymizeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PseudoanonymizeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
