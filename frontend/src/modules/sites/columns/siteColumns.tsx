import type { ColumnDef } from "@tanstack/react-table";
import type { Site } from "../types";
import { DataTableColumnHeader } from "@/components/data-table/DataTableColumnHeader";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { ActionMenuCell } from "@/components/data-table/cells/ActionMenuCell";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { Eye, Edit, ShieldBan } from "lucide-react";

export const siteColumns: ColumnDef<Site>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Site Name" />
    ),
    cell: ({ row }) => {
      const { name, code } = row.original;
      return (
        <div>
          <div className="font-medium whitespace-nowrap">{name}</div>
          <div className="text-xs text-muted-foreground">{code}</div>
        </div>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "status",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Status" />
    ),
    cell: ({ row }) => (
      <StatusBadgeCell 
        status={row.getValue("status")}
        config={{
          "active": { label: "Active", variant: "default" },
          "pre-construction": { label: "Pre-construction", variant: "secondary" },
          "paused": { label: "Paused", variant: "destructive" },
          "completed": { label: "Completed", variant: "outline" },
          "handover": { label: "Handover", variant: "secondary" },
        }}
      />
    ),
    enableSorting: true,
  },
  {
    accessorKey: "supervisor",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Supervisor" />
    ),
    cell: ({ row }) => (
      <div className="truncate max-w-[150px]">{row.getValue("supervisor")}</div>
    ),
    enableSorting: true,
  },
  {
    id: "occupancy",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Occupancy" />
    ),
    cell: ({ row }) => {
      const { current_occupancy, max_occupancy } = row.original;
      const percentage = Math.round((current_occupancy / max_occupancy) * 100);
      return (
        <div className="flex flex-col gap-1">
          <div className="text-sm">
            {current_occupancy} / {max_occupancy}
          </div>
          <div className="h-1.5 w-24 bg-secondary rounded-full overflow-hidden">
            <div 
              className={`h-full ${percentage >= 100 ? "bg-destructive" : percentage > 80 ? "bg-amber-500" : "bg-emerald-500"}`} 
              style={{ width: `${Math.min(percentage, 100)}%` }} 
            />
          </div>
        </div>
      );
    },
    enableSorting: false,
  },
  {
    accessorKey: "municipality",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Municipality" />
    ),
    cell: ({ row }) => (
      <div className="truncate max-w-[150px]">
        {row.getValue("municipality")}
      </div>
    ),
    enableSorting: true,
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const site = row.original;

      return (
        <ActionMenuCell>
          <DropdownMenuItem onClick={() => console.log("View Dashboard", site.id)}>
            <Eye className="mr-2 h-4 w-4" />
            View Dashboard
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => console.log("Edit", site.id)}>
            <Edit className="mr-2 h-4 w-4" />
            Edit Site
          </DropdownMenuItem>
          <DropdownMenuItem 
            className="text-destructive focus:bg-destructive focus:text-destructive-foreground"
            onClick={() => console.log("Suspend", site.id)}
          >
            <ShieldBan className="mr-2 h-4 w-4" />
            Suspend Operations
          </DropdownMenuItem>
        </ActionMenuCell>
      );
    },
  },
];
