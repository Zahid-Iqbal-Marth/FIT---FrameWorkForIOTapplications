import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SensorModalComponent } from './sensor-modal.component';

describe('SensorModalComponent', () => {
  let component: SensorModalComponent;
  let fixture: ComponentFixture<SensorModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SensorModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SensorModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
