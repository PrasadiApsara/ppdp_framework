import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BuildModelComponent } from './build-model/build-model.component';
import { PseudoanonymizeComponent } from './pseudoanonymize/pseudoanonymize.component';
import { KAnonymizeComponent } from './k-anonymize/k-anonymize.component';
import { TwitterLiveComponent } from './twitter-live/twitter-live.component';
import { ExperimentAnonymizeComponent } from './experiment-anonymize/experiment-anonymize.component';
import { ExperimentKanonymizeComponent } from './experiment-kanonymize/experiment-kanonymize.component';
import { ExperimentUtilityComponent } from './experiment-utility/experiment-utility.component';
const routes: Routes = [
    {
        path:'',
        component:PseudoanonymizeComponent
    },
    {
        path:'kanonymize',
        component:KAnonymizeComponent
    },
    {
        path:'twitter-live',
        component:TwitterLiveComponent
    },
    {
      path:'experiment',
      component:ExperimentAnonymizeComponent
    },
    {
      path:'experimentkanonymize',
      component:ExperimentKanonymizeComponent
    },
    {
      path:'experimentUtility',
      component:ExperimentUtilityComponent
    }

];
@NgModule({
    imports: [
      RouterModule.forRoot(routes)
    ],
    exports: [
      RouterModule
    ]
  })
export class AppRoutingModule {}