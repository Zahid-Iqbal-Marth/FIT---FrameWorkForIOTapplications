import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperatorLinkModalComponent } from './operator-link-modal.component';

describe('OperatorLinkModalComponent', () => {
  let component: OperatorLinkModalComponent;
  let fixture: ComponentFixture<OperatorLinkModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OperatorLinkModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OperatorLinkModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
