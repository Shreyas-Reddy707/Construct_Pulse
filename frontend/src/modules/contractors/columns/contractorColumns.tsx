import type { ColumnDef } from "@tanstack/react-table";
import type { Contractor } from "../types";
import { DataTableColumnHeader } from "@/components/data-table/DataTableColumnHeader";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { ActionMenuCell } from "@/components/data-table/cells/ActionMenuCell";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { Eye, Edit, ShieldBan } from "lucide-react";

function getExpiryDisplay(isoDate: string): { text: string; className: string } {
  const expiry = new Date(isoDate);
  const now = new Date();
  const diffMs = expiry.getTime() - now.getTime();
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

  const formatted = expiry.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  if (diffDays < 0) {
    return { text: `${formatted} (Expired)`, className: "text-destructive font-medium" };
  }
  if (diffDays <= 30) {
    return { text: `${formatted} (${diffDays}d)`, className: "text-amber-600 font-medium" };
  }
  return { text: formatted, className: "text-muted-foreground" };
}

export const contractorColumns: ColumnDef<Contractor>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Contractor Name" />
    ),
    cell: ({ row }) => (
      <div className="font-medium whitespace-nowrap">{row.getValue("name")}</div>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "company",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Company" />
    ),
    cell: ({ row }) => (
      <div className="truncate max-w-[150px]">{row.getValue("company")}</div>
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
          suspended: { label: "Suspended", variant: "destructive" },
          expired: { label: "Expired", variant: "outline" },
        }}
      />
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
    accessorKey: "contract_expiry",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Contract Expiry" />
    ),
    cell: ({ row }) => {
      const { text, className } = getExpiryDisplay(row.getValue("contract_expiry"));
      return <div className={className}>{text}</div>;
    },
    enableSorting: true,
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const contractor = row.original;

      return (
        <ActionMenuCell>
          <DropdownMenuItem onClick={() => console.log("View", contractor.id)}>
            <Eye className="mr-2 h-4 w-4" />
            View Details
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => console.log("Edit", contractor.id)}>
            <Edit className="mr-2 h-4 w-4" />
            Edit Contractor
          </DropdownMenuItem>
          <DropdownMenuItem
            className="text-destructive focus:bg-destructive focus:text-destructive-foreground"
            onClick={() => console.log("Suspend", contractor.id)}
          >
            <ShieldBan className="mr-2 h-4 w-4" />
            Suspend
          </DropdownMenuItem>
        </ActionMenuCell>
      );
    },
  },
];
