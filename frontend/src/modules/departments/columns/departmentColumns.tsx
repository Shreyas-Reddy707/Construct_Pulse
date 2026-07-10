import type { ColumnDef } from "@tanstack/react-table";
import type { Department } from "../types";
import { DataTableColumnHeader } from "@/components/data-table/DataTableColumnHeader";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { ActionMenuCell } from "@/components/data-table/cells/ActionMenuCell";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { Eye, Edit, Ban } from "lucide-react";

export const departmentColumns: ColumnDef<Department>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Department Name" />
    ),
    cell: ({ row }) => (
      <div className="font-medium whitespace-nowrap">{row.getValue("name")}</div>
    ),
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
          active: { label: "Active", variant: "default" },
          inactive: { label: "Inactive", variant: "outline" },
          under_review: { label: "Under Review", variant: "secondary" },
        }}
      />
    ),
    enableSorting: true,
  },
  {
    accessorKey: "head",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Department Head" />
    ),
    cell: ({ row }) => (
      <div className="truncate max-w-[150px]">{row.getValue("head")}</div>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "worker_count",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Workers" />
    ),
    cell: ({ row }) => (
      <div className="tabular-nums">{row.getValue("worker_count")}</div>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "assigned_sites",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Assigned Sites" />
    ),
    cell: ({ row }) => {
      const sites = row.getValue("assigned_sites") as string[];
      if (!sites || sites.length === 0) {
        return <span className="text-muted-foreground italic">None</span>;
      }
      return (
        <div className="truncate max-w-[200px]" title={sites.join(", ")}>
          {sites.length <= 2 ? sites.join(", ") : `${sites[0]}, +${sites.length - 1} more`}
        </div>
      );
    },
    enableSorting: false,
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const department = row.original;

      return (
        <ActionMenuCell>
          <DropdownMenuItem onClick={() => console.log("View", department.id)}>
            <Eye className="mr-2 h-4 w-4" />
            View Details
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => console.log("Edit", department.id)}>
            <Edit className="mr-2 h-4 w-4" />
            Edit Department
          </DropdownMenuItem>
          <DropdownMenuItem
            className="text-destructive focus:bg-destructive focus:text-destructive-foreground"
            onClick={() => console.log("Deactivate", department.id)}
          >
            <Ban className="mr-2 h-4 w-4" />
            Deactivate
          </DropdownMenuItem>
        </ActionMenuCell>
      );
    },
  },
];
