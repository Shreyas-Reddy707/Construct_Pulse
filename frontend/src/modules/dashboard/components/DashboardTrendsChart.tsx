import { 
  Area, 
  AreaChart, 
  CartesianGrid, 
  Legend, 
  Line, 
  ResponsiveContainer, 
  Tooltip, 
  XAxis, 
  YAxis 
} from "recharts";
import type { DashboardTrendItem } from "../types";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle } from "lucide-react";

interface DashboardTrendsChartProps {
  data?: DashboardTrendItem[];
  isLoading: boolean;
  isError: boolean;
}

export function DashboardTrendsChart({ data, isLoading, isError }: DashboardTrendsChartProps) {
  if (isError) {
    return (
      <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6 min-h-[300px] flex items-center justify-center lg:col-span-2">
        <div className="flex items-center gap-3 text-destructive p-4 border border-destructive/20 rounded-lg bg-destructive/10 max-w-md">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <p className="text-sm font-medium">
            Failed to load workforce trends. Please try again later.
          </p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6 min-h-[300px] flex flex-col justify-between space-y-4 lg:col-span-2">
        <h3 className="font-semibold tracking-tight">Workforce Trends (Last 7 Days)</h3>
        <Skeleton className="w-full flex-1 min-h-[220px]" />
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6 min-h-[300px] flex flex-col justify-between lg:col-span-2">
        <h3 className="font-semibold tracking-tight">Workforce Trends (Last 7 Days)</h3>
        <div className="flex-1 flex items-center justify-center">
          <p className="text-sm text-muted-foreground">No trend data available for this period.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6 min-h-[300px] flex flex-col lg:col-span-2 min-w-0">
      <h3 className="font-semibold tracking-tight mb-4">Workforce Trends (Last 7 Days)</h3>
      <div className="flex-1 min-h-[220px] min-w-0">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorHeadcount" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
            <XAxis 
              dataKey="date" 
              tickFormatter={(val) => {
                const date = new Date(val);
                // Return UTC date string like 10/1
                return `${date.getUTCMonth() + 1}/${date.getUTCDate()}`;
              }}
              tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
              tickLine={false}
              axisLine={false}
              dy={10}
            />
            <YAxis 
              tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
              tickLine={false}
              axisLine={false}
              dx={-10}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: "hsl(var(--popover))", 
                borderColor: "hsl(var(--border))",
                color: "hsl(var(--popover-foreground))",
                borderRadius: "var(--radius)"
              }}
              labelFormatter={(label) => new Date(label).toLocaleDateString()}
            />
            <Legend wrapperStyle={{ paddingTop: "20px", fontSize: "12px", color: "hsl(var(--foreground))" }} />
            <Area 
              type="monotone" 
              dataKey="headcount" 
              name="Headcount"
              stroke="hsl(var(--primary))" 
              strokeWidth={2}
              fillOpacity={1} 
              fill="url(#colorHeadcount)" 
            />
            <Line 
              type="monotone" 
              dataKey="hours" 
              name="Total Hours"
              stroke="hsl(var(--chart-2, 220 70% 50%))" 
              strokeWidth={2}
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
