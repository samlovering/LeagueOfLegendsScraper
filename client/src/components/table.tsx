// Table.tsx
import { AgGridReact } from "ag-grid-react";
import type { ColDef } from "ag-grid-community";

import { ModuleRegistry, AllCommunityModule, themeAlpine } from 'ag-grid-community';
    
ModuleRegistry.registerModules([ AllCommunityModule ]);


type TableProps<T> = {
  rowData: T[];
  columnDefs: ColDef<T>[];
  className?: string;
  onRowClicked?: (row: T) => void;
};

function Table<T>({ 
  rowData, 
  columnDefs, 
  className = "ag-theme-alpine", 
  onRowClicked 
}: TableProps<T>) {
  return (
    <div className={className} style={{ height: "500px", width: "100%" }}>
      <AgGridReact
        theme={themeAlpine}
        rowData={rowData}
        columnDefs={columnDefs}
        onRowClicked={(e) => onRowClicked?.(e.data as T)}
        onGridReady={params => params.api.sizeColumnsToFit()}
      />
    </div>
  );
}

export default Table;
