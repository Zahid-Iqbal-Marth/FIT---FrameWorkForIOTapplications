
import { Component, OnInit, Optional, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';


@Component({
  selector: 'app-sensor-modal',
  templateUrl: './sensor-modal.component.html',
  styleUrls: ['./sensor-modal.component.css']
})
export class SensorModalComponent implements OnInit {

  config_data : string;
  selectedType : string;

  avaliableSensors;



  constructor(
    //this received the data from app-component
    public dialogRef: MatDialogRef<SensorModalComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.avaliableSensors = data.avaliableSensors;
  }

  ngOnInit() {
  }

  closeDialog() {// this is called when sensor-model is closed
     // this closes the model and return the data to app-component
    this.dialogRef.close({ event: 'close', data: { 
      config_data : {
        config_data : this.config_data,
      },
      type :this.selectedType
    } });
  }


}
