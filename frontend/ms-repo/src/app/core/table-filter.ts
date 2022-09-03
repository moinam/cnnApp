import { NgModule } from '@angular/core';

import { TableFilterPipe } from './table-filter.pipe';

@NgModule({
  declarations: [TableFilterPipe],
  exports: [TableFilterPipe],
})
export class TableFilterModule {}
