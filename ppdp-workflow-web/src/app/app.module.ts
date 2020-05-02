import { BrowserModule } from '@angular/platform-browser';
import { NgModule, PipeTransform, Pipe } from '@angular/core';
import { MatInputModule, MatButtonModule, MatSelectModule, MatIconModule, MatSidenavModule, MatCheckboxModule, MatToolbarModule, MatDividerModule, MatListModule, MatCardModule, MatProgressSpinnerModule, MatChipsModule } from '@angular/material';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NavbarComponent } from './navbar/navbar.component';
import { AppRoutingModule } from './app-routing.module';
import { BuildModelComponent } from './build-model/build-model.component';
import { TwitterLiveComponent } from './twitter-live/twitter-live.component';
import { KAnonymizeComponent } from './k-anonymize/k-anonymize.component';
import { ToolBarComponent } from './tool-bar/tool-bar.component';
import { PseudoanonymizeComponent } from './pseudoanonymize/pseudoanonymize.component';
import { GoogleChartsModule } from 'angular-google-charts';
import { FlexLayoutModule } from '@angular/flex-layout';
import { HttpClientModule } from '@angular/common/http';
import { DataService } from './data.service';
import {MatTableModule} from '@angular/material/table';
import { ExperimentAnonymizeComponent } from './experiment-anonymize/experiment-anonymize.component';
import { SafeHtmlPipe } from './safe-html.pipe';
import { CommonModule } from '@angular/common';
import { MainPipeModule } from './main-pipe/main-pipe.module';
import { ExperimentKanonymizeComponent } from './experiment-kanonymize/experiment-kanonymize.component';
import { ExperimentUtilityComponent } from './experiment-utility/experiment-utility.component';
import {MatExpansionModule} from '@angular/material/expansion';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    BuildModelComponent,
    TwitterLiveComponent,
    KAnonymizeComponent,
    ToolBarComponent,
    PseudoanonymizeComponent,
    ExperimentAnonymizeComponent,
    ExperimentKanonymizeComponent,
    ExperimentUtilityComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatIconModule,
    MatSidenavModule,
    MatCheckboxModule, 
    MatToolbarModule,
    MatDividerModule,
    MatListModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatInputModule,
    GoogleChartsModule,
    FlexLayoutModule, 
    AppRoutingModule,
    HttpClientModule,
    MatTableModule,
    MainPipeModule,
    MatExpansionModule
  ],
  providers: [DataService, SafeHtmlPipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
