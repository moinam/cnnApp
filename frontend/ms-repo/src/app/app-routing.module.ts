import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent} from "./dashboard/dashboard.component"
import { SupportComponent } from "./support/support.component"

const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'support', component: SupportComponent},
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: '**', redirectTo: 'dashboard', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
