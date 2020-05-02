import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KAnonymizeComponent } from './k-anonymize.component';

describe('KAnonymizeComponent', () => {
  let component: KAnonymizeComponent;
  let fixture: ComponentFixture<KAnonymizeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KAnonymizeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KAnonymizeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
