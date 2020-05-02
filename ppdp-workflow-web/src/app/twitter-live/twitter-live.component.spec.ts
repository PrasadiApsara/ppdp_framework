import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TwitterLiveComponent } from './twitter-live.component';

describe('TwitterLiveComponent', () => {
  let component: TwitterLiveComponent;
  let fixture: ComponentFixture<TwitterLiveComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TwitterLiveComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TwitterLiveComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
