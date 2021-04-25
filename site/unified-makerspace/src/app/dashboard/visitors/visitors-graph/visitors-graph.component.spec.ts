import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VisitorsGraphComponent } from './visitors-graph.component';

describe('UserGraphComponent', () => {
  let component: VisitorsGraphComponent;
  let fixture: ComponentFixture<VisitorsGraphComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [VisitorsGraphComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VisitorsGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
