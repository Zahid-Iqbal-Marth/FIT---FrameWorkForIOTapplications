import { Component, OnInit, Optional, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {FormControl, FormGroup} from '@angular/forms';
import {FormlyFieldConfig} from '@ngx-formly/core';

@Component({
  selector: 'app-operator-link-modal',
  templateUrl: './operator-link-modal.component.html',
  styleUrls: ['./operator-link-modal.component.css']
})
export class OperatorLinkModalComponent implements OnInit {


  
  form = new FormGroup({});
  model = {};


  //arg required for HR_filter     
    Filter_args_fields: FormlyFieldConfig[] = [
      {
        key: 'lower_bound',
        type: 'input',
        templateOptions: {
          label: 'Lower Bound',
          placeholder: 'Enter value inside the range of incomming data',
          type : 'number',
          required: true,
        }
      },
      {
        key: 'upper_bound',
        type: 'input',
        templateOptions: {
          label: 'Upper Bound',
          placeholder: 'Enter value inside the range of incomming data',
          type : 'number',
          required: true,
        }
      },
    ]


  



  //arg required for HR_filter     
  EdgeDetector_args_fields: FormlyFieldConfig[] = [
    {
      key: 'lower_bound',
      type: 'input',
      templateOptions: {
        label: 'Lower Bound For Canny Edge Detector',
        placeholder: 'Enter value inside the range 0-255',
        min : 0,
        max : 255,
        type : 'number',
        required: true,
      }
    },
    {
      key: 'upper_bound',
      type: 'input',
      templateOptions: {
        label: 'Upper Bound For Canny Edge Detector',
        placeholder: 'Enter value inside the range 0-255',
        min : 0,
        max : 255,
        type : 'number',
        required: true,
      }
    },
  ]
  


  //arge require for Human_Actitivty_Recognation
  HAR_args_fields: FormlyFieldConfig[] = [

    {
      key: 'selected_activities',
      type: 'select',
      templateOptions: {
        label: 'Activities',
        multiple : true,
        required: true,
        options: [
          { label: 'WALKING', value: 'WALKING' },
          { label: 'WALKING_UPSTAIRS', value: 'WALKING_UPSTAIRS' },
          { label: 'WALKING_DOWNSTAIRS', value: 'WALKING_DOWNSTAIRS' },
          { label: 'SITTING', value: 'SITTING' },
          { label: 'STANDING', value: 'STANDING' },
          { label: 'LAYING', value: 'LAYING' },
        ]
      }
    },


  ]



    //arg required for HR_filter     
    Logical_op_args_fields: FormlyFieldConfig[] = [
      {
        key: 'type',
        type: 'select',
        templateOptions: {
          label: 'Type',
          placeholder: 'AND || OR',
          required: true,
          options: [
            { label: 'AND', value: 'AND' },
            { label: 'OR', value: 'OR' },
          ]
        }
      },

    ]



    //arg required for HR_filter     
    Alert_args_fields: FormlyFieldConfig[] = [
      {
        key: 'time_window',
        type: 'input',

        templateOptions: {
          label: 'Time Window',
          placeholder: 'Used for sync',
          type : 'number',
          required: false,
        }
      },
      {
        key: 'alert_message',
        type: 'input',
        defaultValue : '',
        templateOptions: {
          label: 'Alert Message (optional)',
          placeholder: 'Optional',
          required: false,
        }
      },
      {
        key: 'alert_dest',
        type: 'input',
        defaultValue : '',
        templateOptions: {
          label: "Receiver's Email (optional)",
          placeholder: 'Optional',
          required: false,
        }
      },

    ]



  // this function uses the compatibility array it
  // received from app-component and check the compatibility of 
  // selected oprtator
  check_compatibility(){

    this.comp_Nodes = []

    this.Nodes.forEach(node => {

          this.compatibility[this.OperatorType].forEach(comp_nodes => {
              if (node.split("-")[1] == comp_nodes){

                this.comp_Nodes.push(node)

              }
          });

    });

    this.select_Nodes = true;

  }







  Nodes: any;
  avaliableOperator : any;
  compatibility : any;

  comp_Nodes = [];
  
  fromDialog: string;


  select_Nodes = false;


  // sources will hold the nodes which are giving input to the selected operator
  Sources = new FormControl();
  //this will hold the selected operator type
  OperatorType: any;

  custom_name = "";



  constructor(


    //this received the data from app-component
    public dialogRef: MatDialogRef<OperatorLinkModalComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.Nodes = data.Nodes;
    this.avaliableOperator = data.avaliableOperator;
    this.compatibility = data.compatibility
  }

  ngOnInit(): void {
  }



  // this is called when operator-model is closed
  closeDialog() {


    if (this.model['time_window'] == null){
      this.model['time_window'] = 0;
    }
    if (this.form.valid) {
      console.log(this.model);
    }

    if (this.custom_name == ""){
      this.custom_name = this.OperatorType
    }
    // this closes the model and return the data to app-component
    this.dialogRef.close({ event: 'close', data: {
      source : this.Sources.value,
      type : this.OperatorType,
      custom_name : this.custom_name,

      config_data : this.model

    } });
  }

}
