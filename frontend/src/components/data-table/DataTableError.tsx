import { TableCell, TableRow } from "@/components/ui/table";
import { AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

interface DataTableErrorProps {
  columnCount: number;
  onRetry?: () => void;
}

export function DataTableError({ columnCount, onRetry }: DataTableErrorProps) {
  return (
    <TableRow>
      <TableCell colSpan={columnCount} className="h-48 text-center">
        <div className="flex flex-col items-center justify-center text-destructive">
          <AlertTriangle className="h-8 w-8 mb-4 text-destructive/50" />
          <p className="mb-4">An error occurred while fetching data.</p>
          {onRetry && (
            <Button variant="outline" onClick={onRetry}>
              Try again
            </Button>
          )}
        </div>
      </TableCell>
    </TableRow>
  );
}
