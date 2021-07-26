import { Component, OnInit, Optional, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {FormControl, FormGroup} from '@angular/forms';
import {FormlyFieldConfig} from '@ngx-formly/core';

@Component({
  selector: 'app-deployment',
  templateUrl: './deployment.component.html',
  styleUrls: ['./deployment.component.css']
})
export class DeploymentComponent implements OnInit {


  form = new FormGroup({});
  model = {};

    //arg required for HR_filter     
    form_fields: FormlyFieldConfig[] = [
      {
        key: 'deploy_device_ip',
        type: 'input',
        templateOptions: {
          label: 'Destination IP',
          placeholder: 'Enter the Destination IP',
          required: true,
        }
      },
      {
        key: 'device_username',
        type: 'input',
        templateOptions: {
          label: 'Destination Username',
          placeholder: 'Enter the Destination Username',
          required: false,
        }
      },
      {
        key: 'device_pass',
        type: 'input',
        templateOptions: {
          label: 'Destination Password',
          placeholder: 'Enter the Destination Password',
          required: false,
          type : 'password'
        }
      },
    ]



  deploy_device_ip : string;
  device_username : string;
  device_pass : string;


  constructor(
    //this received the data from app-component
    public dialogRef: MatDialogRef<DeploymentComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    
  }

  ngOnInit() {
  }

  closeDialog() {// this is called when sensor-model is closed
     // this closes the model and return the data to app-component
    this.dialogRef.close({ event: 'close', data: { 

      deploy_device_ip : this.model['deploy_device_ip'],
      device_username : this.model['device_username'],
      device_pass : this.model['device_pass']
    

    } });
  }


}
