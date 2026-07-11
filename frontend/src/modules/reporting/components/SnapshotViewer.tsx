import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent } from "@/components/ui/card";

interface SnapshotViewerProps {
  data: Record<string, any>;
}

export function SnapshotViewer({ data }: SnapshotViewerProps) {
  return (
    <div className="space-y-4">
      {Object.entries(data).map(([key, value]) => (
        <SnapshotNode key={key} nodeKey={key} value={value} />
      ))}
    </div>
  );
}

function SnapshotNode({ nodeKey, value }: { nodeKey: string; value: any }) {
  const formatKey = (k: string) => k.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());

  if (value === null || value === undefined) {
    return (
      <div className="flex gap-2">
        <span className="font-medium">{formatKey(nodeKey)}:</span>
        <span className="text-muted-foreground italic">N/A</span>
      </div>
    );
  }

  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return (
      <div className="flex gap-2">
        <span className="font-medium">{formatKey(nodeKey)}:</span>
        <span>{value.toString()}</span>
      </div>
    );
  }

  if (Array.isArray(value)) {
    if (value.length === 0) {
      return (
        <div className="flex gap-2">
          <span className="font-medium">{formatKey(nodeKey)}:</span>
          <span className="text-muted-foreground italic">Empty List</span>
        </div>
      );
    }
    
    // If it's an array of objects, render a table
    if (typeof value[0] === "object" && value[0] !== null) {
      const columns = Array.from(new Set(value.flatMap(Object.keys)));
      return (
        <Card>
          <CardContent className="pt-6">
            <h4 className="font-semibold mb-4">{formatKey(nodeKey)}</h4>
            <div className="rounded-md border overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    {columns.map((col) => (
                      <TableHead key={col}>{formatKey(col)}</TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {value.map((item, i) => (
                    <TableRow key={i}>
                      {columns.map((col) => (
                        <TableCell key={col}>
                          {typeof item[col] === "object" 
                            ? JSON.stringify(item[col]) 
                            : String(item[col] ?? "-")}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      );
    }

    // Array of primitives
    return (
      <div className="flex gap-2">
        <span className="font-medium">{formatKey(nodeKey)}:</span>
        <span>{value.join(", ")}</span>
      </div>
    );
  }

  if (typeof value === "object") {
    return (
      <Card>
        <CardContent className="pt-6">
          <h4 className="font-semibold mb-4">{formatKey(nodeKey)}</h4>
          <div className="pl-4 border-l-2 border-muted space-y-2">
            {Object.entries(value).map(([k, v]) => (
              <SnapshotNode key={k} nodeKey={k} value={v} />
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return null;
}
