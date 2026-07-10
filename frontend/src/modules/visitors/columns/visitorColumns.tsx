import type { ColumnDef } from "@tanstack/react-table";
import type { Visitor } from "../types";
import { DataTableColumnHeader } from "@/components/data-table/DataTableColumnHeader";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { ActionMenuCell } from "@/components/data-table/cells/ActionMenuCell";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { Eye, LogOut, Ban } from "lucide-react";

function formatCheckInTime(isoDate: string | null): string {
  if (!isoDate) return "—";
  const date = new Date(isoDate);
  return date.toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export const visitorColumns: ColumnDef<Visitor>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Visitor Name" />
    ),
    cell: ({ row }) => {
      const company = row.original.company;
      return (
        <div>
          <div className="font-medium whitespace-nowrap">{row.getValue("name")}</div>
          {company && <div className="text-xs text-muted-foreground">{company}</div>}
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
          scheduled: { label: "Scheduled", variant: "outline" },
          checked_in: { label: "Checked In", variant: "default" },
          checked_out: { label: "Checked Out", variant: "secondary" },
          denied: { label: "Denied", variant: "destructive" },
        }}
      />
    ),
    enableSorting: true,
  },
  {
    accessorKey: "host",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Host" />
    ),
    cell: ({ row }) => (
      <div className="truncate max-w-[150px]">{row.getValue("host")}</div>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "site",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Site" />
    ),
    cell: ({ row }) => (
      <div className="truncate max-w-[150px]">{row.getValue("site")}</div>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "purpose",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Purpose" />
    ),
    cell: ({ row }) => (
      <div className="truncate max-w-[150px] text-muted-foreground">{row.getValue("purpose")}</div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: "check_in",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Check-In Time" />
    ),
    cell: ({ row }) => (
      <div className="font-medium">{formatCheckInTime(row.getValue("check_in"))}</div>
    ),
    enableSorting: true,
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const visitor = row.original;
      
      return (
        <ActionMenuCell>
          <DropdownMenuItem onClick={() => console.log("View", visitor.id)}>
            <Eye className="mr-2 h-4 w-4" />
            View Details
          </DropdownMenuItem>
          {visitor.status === "checked_in" && (
            <DropdownMenuItem onClick={() => console.log("Checkout", visitor.id)}>
              <LogOut className="mr-2 h-4 w-4" />
              Check Out
            </DropdownMenuItem>
          )}
          {visitor.status === "scheduled" && (
            <DropdownMenuItem
              className="text-destructive focus:bg-destructive focus:text-destructive-foreground"
              onClick={() => console.log("Deny", visitor.id)}
            >
              <Ban className="mr-2 h-4 w-4" />
              Deny Access
            </DropdownMenuItem>
          )}
        </ActionMenuCell>
      );
    },
  },
];
