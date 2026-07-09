import type { ColumnDef } from "@tanstack/react-table";
import type { Worker } from "../types";
import { DataTableColumnHeader } from "@/components/data-table/DataTableColumnHeader";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { ActionMenuCell } from "@/components/data-table/cells/ActionMenuCell";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { Eye, Edit, ShieldBan } from "lucide-react";

export const workerColumns: ColumnDef<Worker>[] = [
  {
    accessorKey: "first_name",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Name" />
    ),
    cell: ({ row }) => {
      const { first_name, last_name } = row.original;
      return (
        <div className="font-medium whitespace-nowrap">
          {first_name} {last_name}
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
    cell: ({ row }) => <StatusBadgeCell status={row.getValue("status")} />,
    enableSorting: true,
  },
  {
    accessorKey: "role",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Role" />
    ),
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("role")}</div>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "current_site",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Current Site" />
    ),
    cell: ({ row }) => {
      const site = row.getValue("current_site") as string | null;
      return site ? (
        <span className="truncate max-w-[150px] block">{site}</span>
      ) : (
        <span className="text-muted-foreground italic">Unassigned</span>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "department",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Department" />
    ),
    cell: ({ row }) => (
      <div className="truncate max-w-[150px]">
        {row.getValue("department")}
      </div>
    ),
    enableSorting: true,
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const worker = row.original;

      return (
        <ActionMenuCell>
          <DropdownMenuItem onClick={() => console.log("View", worker.id)}>
            <Eye className="mr-2 h-4 w-4" />
            View Details
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => console.log("Edit", worker.id)}>
            <Edit className="mr-2 h-4 w-4" />
            Edit Worker
          </DropdownMenuItem>
          <DropdownMenuItem 
            className="text-destructive focus:bg-destructive focus:text-destructive-foreground"
            onClick={() => console.log("Suspend", worker.id)}
          >
            <ShieldBan className="mr-2 h-4 w-4" />
            Suspend
          </DropdownMenuItem>
        </ActionMenuCell>
      );
    },
  },
];
