import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {NgxGraphModule} from  '@swimlane/ngx-graph';

import { FormlyModule } from '@ngx-formly/core';
import { FormlyMaterialModule } from '@ngx-formly/material';


import { FormsModule , ReactiveFormsModule} from '@angular/forms';

// Material UI Modules
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialogModule } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatTabsModule} from '@angular/material/tabs';
import {MatTreeModule} from '@angular/material/tree';
import {MatIconModule} from '@angular/material/icon';
import {CdkTreeModule} from '@angular/cdk/tree';

import { SensorModalComponent } from './modals/sensor-modal/sensor-modal.component';
import { OperatorLinkModalComponent } from './modals/operator-link-modal/operator-link-modal.component';


import { HttpClientModule } from "@angular/common/http";
import { DeploymentComponent } from './modals/deployment/deployment.component'

@NgModule({
  declarations: [
    AppComponent,
    SensorModalComponent,
    OperatorLinkModalComponent,
    DeploymentComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    DragDropModule,
    NgxGraphModule,

    FormsModule,
    MatFormFieldModule,
    MatDialogModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatTooltipModule,
    MatTabsModule,
    MatTreeModule,
    MatIconModule,
    CdkTreeModule,

    ReactiveFormsModule,

    FormlyModule.forRoot({
      validationMessages: [
        { name: 'required', message: 'This field is required' },
      ],
    }),
    FormlyMaterialModule,

    HttpClientModule,

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
