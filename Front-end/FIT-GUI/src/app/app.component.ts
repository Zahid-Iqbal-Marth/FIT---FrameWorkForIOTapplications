import { Component, ViewChild, ElementRef } from '@angular/core';
import { Node, Edge, ClusterNode } from '@swimlane/ngx-graph';

import { MatDialog } from '@angular/material/dialog';
import { SensorModalComponent } from 'src/app/modals/sensor-modal/sensor-modal.component';

import { OperatorLinkModalComponent } from 'src/app/modals/operator-link-modal/operator-link-modal.component';
import { stringify } from 'querystring';
import { GenCodeService } from './gen-code.service';

import {NestedTreeControl} from '@angular/cdk/tree';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import { DeploymentComponent } from './modals/deployment/deployment.component';




/**
 * Food data with nested structure.
 * Each node has a name and an optional list of children.
 */
 interface FoodNode {
  name: string;
  children?: FoodNode[];
}

const TREE_DATA: FoodNode[] = [
  {
    name: 'Project Overview',
    children: [
      {name: "FIT is a framework that allows users to create complex IoT applications that involve stream processing, event processing, and complex event processing. FIT is a generic framework aimed to be usable by the diverse users of CEP. A GUI is built upon the framework for generic as well as specific applications. Our GUI will enable users add some components to create the application's pipeline."},
    ]
  }, {
    name: 'Sensors',
    children: [
      {
        name: 'It will provide data in the form of streams from sensors(we will use Virtual sensors to test our application).',
      },
    ]
  }, {
    name: 'Operators',
    children: [
      {
        name: "Which can contain different functionalities such as object detection Algorithm, fall detection Algorithm, etc",
        
      },
      {
        name: 'Input',
        children : [{
          name: "From one or more sensors or operators",
        }
        ]
      }, {
        name: 'Output',
        children : [{
          name: "Single – result of the applied algorithm",
        }
        ]
      },
    ]
  },
  {
    name: 'Alerts',
    children: [
      {
        name: 'Messages/Triggers/Automated Actions.'},
    ]
  },
  {
    name: 'Proof of concept',
    children: [
      {
        name: 'As a proof of concept we will add different sensors, operators and alerts that can be found in old homes. This will enable caretakers to create complex scenarios by using a simple configurable graphical user interface. It will help them to automate old homes according to the needs of each individual resident. Our framework will also help users to deploy and run these scenarios on different remote machines.'},
    ]
  },
  {
    name: 'List of Dependencies',
    children: [
      {
        name: "To install Dependencies and Settingup the application you just have to download setup_FIT_Application.sh and run it."},
      {
        name: "It will download the code from github, install all the Dependencies and start all servers requied to run the application"},
        
    ]

  },
  {
    name: 'Github Repository',
    children: [
      {
        name: 'https://github.com/Zahid-Iqbal-Marth/FIT---FrameWorkForIOTapplications'},
    ]
  },


];



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers : [GenCodeService]
})
export class AppComponent { 





  treeControl = new NestedTreeControl<FoodNode>(node => node.children);
  dataSource = new MatTreeNestedDataSource<FoodNode>();

  hasChild = (_: number, node: FoodNode) => !!node.children && node.children.length > 0;







  constructor(
    public dialog: MatDialog,
    private gencodeService : GenCodeService
    
  ) { 
    this.dataSource.data = TREE_DATA;
  }


  title = 'FIT-GUI';


  // these counters will be added to Sensors/Operators names for uniquness if they are selected more the once
  Sensorcount = 1;
  Operatorcount = 1;



  // these contains the list of avalible sensots and operators
  avaliableSensors = ['Heart_Rate', 'Surveillance_Camera', 'Accelerometer', 'Gyroscope'];
  avaliableOperator = ['Filter', 'Edge_detection', 'Noise_Removel', 'Fall_detection',  'Human_Activity_Recognition', 'Logical_Operator'];


  // this is the compatibility list which will be passed to operator-model
  compatibility = {
    'Filter' : ['Heart_Rate'],
    'Edge_detection' : ['Surveillance_Camera'],
    'Noise_Removel' : ['Surveillance_Camera'],
    'Fall_detection' : ['Surveillance_Camera'],
    'Logical_Operator' : ['Human_Activity_Recognition', 'Filter', 'Logical_Operator'],
    'Human_Activity_Recognition' : ['Accelerometer', 'Gyroscope']
  }

  //this contains the logos on avalible sensors
  avaliableSensorsLogos = {
    'Heart_Rate' : 'https://www.pngitem.com/pimgs/m/119-1197929_heartbeat-heart-rate-monitor-icon-hd-png-download.png',
    'Surveillance_Camera' : 'https://cdn0.iconfinder.com/data/icons/gambling-23/50/23-512.png',
    'Accelerometer' : 'https://i.imgur.com/7qR5OZJ.png',
    'Gyroscope' : 'https://i.pinimg.com/originals/05/c7/79/05c7790d6614191b50d82c8ab9e2b42a.png',
  }


  // this will hold the links between the nodes
  Links   = [];

  // this will hold the nodes(sensors.operators)
  Nodes  = [];


  //hepls to take record of real name of operator when custom name is used
  Lable_id_dict = {};


  //this will hold the json which we'll send to back-end and use that to generate conroller class
  Send_to_Backend = {};



  // dialogValue: string;
  // sendValue: string;



  newNode; // temp node which is used to receive the data from models (sensors/operators)

  nodeList = []; // contains the list of node labels which are sent to operator model



	// this function will be called when user clicks on add sensor button
  addSensor(): void {
	// send data to sensor-model
    const dialogRef = this.dialog.open(SensorModalComponent, {
      width: '500px',
      backdropClass: 'custom-dialog-backdrop-class',
      panelClass: 'custom-dialog-panel-class',
      data: { avaliableSensors: this.avaliableSensors }
    });
	
	// called when model is closed and then receives data
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.newNode = {
        id :  'S' + this.Sensorcount + '-' + result.data.type,
        label : 'S' + this.Sensorcount + '-' + result.data.type,
        class_name : result.data.type,  // matches with backend class names , helps to create objects
        type : "sensors",
        config_data : result.data.config_data, // this can be either IP or filename
        produce_to_topic : "" , // this will be filled latter
        consume_from_topic : [], // this will be filled latter
        meta: { // used at front-end
          link: this.avaliableSensorsLogos[result.data.type],
          url: ""
        }
      };



	// make entry in a dic which'll be sent to backend

      this.Send_to_Backend[this.newNode.id] = this.newNode



	

      //hepls to take record of real name of operator when custom name is used
      this.Lable_id_dict[this.newNode.label] = this.newNode.id


	// adding a new node

        this.Nodes.push(this.newNode);
        this.Nodes = [...this.Nodes];

        this.nodeList.push(this.newNode.label );
        this.Sensorcount += 1;
    });
  }



 // this function will be called when user clicks on add sensor button
  addOperator(): void {
    	// send data to operator-model
    const dialogRef = this.dialog.open(OperatorLinkModalComponent, {
      width: '500px',
      backdropClass: 'custom-dialog-backdrop-class',
      panelClass: 'custom-dialog-panel-class',
      data: { IsOperator: true,
              Nodes :  this.nodeList,
              avaliableOperator : this.avaliableOperator,
              compatibility : this.compatibility}
    });


    // called when model is closed and then receives data
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);

    var opt_logo = 'https://img2.pngio.com/azure-stream-analytics-synegrate-trusted-business-azure-stream-analytics-png-512_512.png'

      this.newNode = {
        id :  'O' + this.Operatorcount + '-' + result.data.type,
        label : 'O' + this.Operatorcount + '-' + result.data.custom_name,
	class_name : result.data.type,  // matches with backend class names , helps to create objects
        type : "operators",
        config_data : result.data.config_data, // this will contain config data for operators
        produce_to_topic : "" , //this will be filled later
        consume_from_topic : [],  //this will be filled later
        meta: { // used at front-end
          link: opt_logo,
          url: ""
        }
      };




	// make entry in a dic which'll be sent to backend

      this.Send_to_Backend[this.newNode.id] = this.newNode





 //hepls to take record of real name of operator when custom name is used
      this.Lable_id_dict[this.newNode.label] = this.newNode.id


      	// adding a new node
      this.Nodes.push(this.newNode);
      this.Nodes = [...this.Nodes];
      this.nodeList.push(this.newNode.label);

      // console.log(this.Nodes);


      //now adding links between the selected nodes(sensors/operator) and seleted operator
      var i = 0;
      while( result.data.source[i]){ // loop on all the sources from which the new-added / seleted operator is taking data
          this.newNode = { 
            id: 'label' + i.toString() + this.Operatorcount.toString(),
            source: this.Lable_id_dict[result.data.source[i]],
            target: 'O' + this.Operatorcount + '-' + result.data.type 
          };

          var topic_name = this.newNode.source// + "," + this.newNode.target

          // making source and destination/target entries to Send_to_Backend [] which will be used to send data b/w diff nodes
	  
          if (this.Send_to_Backend[this.newNode.source].produce_to_topic == ""){
              this.Send_to_Backend[this.newNode.source].produce_to_topic = topic_name
          }
          this.Send_to_Backend[this.newNode.target].consume_from_topic.push(topic_name)

          // console.log(this.newNode);
          //puses the newly created Link into the Links []
          this.Links.push(this.newNode);
          this.Links = [...this.Links];
          i += 1;
      }



      




      this.Operatorcount += 1;







    });
  }




	// this function will be called when user clicks on add sensor button
  deploy(): void {
    // send data to sensor-model
      const dialogRef = this.dialog.open(DeploymentComponent, {
        width: '500px',
        backdropClass: 'custom-dialog-backdrop-class',
        panelClass: 'custom-dialog-panel-class',
        data: { }
      });
    
    // called when model is closed and then receives data
      dialogRef.afterClosed().subscribe(result => {
        console.log('The dialog was closed', result);
        this.newNode = {
          deploy_device_ip : result.data.deploy_device_ip,
          device_username : result.data.device_username,
          device_pass : result.data.device_pass
        };
  
  
  
    // make entry in a dic which'll be sent to backend
        
        this.Send_to_Backend["Deploy_info"] = this.newNode
        this.onCompletion()
      });
    }
  





  // used when user finishes ccreating pipeline
  onCompletion(){

    console.log(JSON.stringify(this.Send_to_Backend, null, 2))
    this.genCode()


  }

  // sends Send_to_Backend[] to back-end
  genCode(){

    var data = JSON.stringify(this.Send_to_Backend, null, 2)
    this.gencodeService.Generate_Code(data)
      .subscribe(
         data=> {
           console.log('Code is generated')
         },
         error => console.log(error)

      )

  }


































}
