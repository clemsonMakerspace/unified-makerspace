import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VisitorsTableComponent } from './visitors-table.component';

describe('UserTableComponent', () => {
  let component: VisitorsTableComponent;
  let fixture: ComponentFixture<VisitorsTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VisitorsTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VisitorsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
