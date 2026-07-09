import { TableCell, TableRow } from "@/components/ui/table";
import { FolderX } from "lucide-react";

interface DataTableEmptyProps {
  columnCount: number;
}

export function DataTableEmpty({ columnCount }: DataTableEmptyProps) {
  return (
    <TableRow>
      <TableCell colSpan={columnCount} className="h-48 text-center">
        <div className="flex flex-col items-center justify-center text-muted-foreground">
          <FolderX className="h-8 w-8 mb-4 text-muted-foreground/50" />
          <p>No results found.</p>
        </div>
      </TableCell>
    </TableRow>
  );
}
