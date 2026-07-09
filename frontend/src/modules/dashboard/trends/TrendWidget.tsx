import { useDashboardTrends } from "../hooks/useDashboardQueries";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { Area, AreaChart, CartesianGrid, XAxis, ResponsiveContainer } from "recharts";

interface TrendWidgetProps {
  className?: string;
}

export function TrendWidget({ className }: TrendWidgetProps) {
  const { data, isLoading, isError } = useDashboardTrends();

  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <Skeleton className="h-6 w-1/4" />
          <Skeleton className="h-4 w-1/3 mt-2" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-[300px] w-full" />
        </CardContent>
      </Card>
    );
  }

  if (isError || !data) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <div className="text-sm text-destructive">Failed to load trend data.</div>
        </CardContent>
      </Card>
    );
  }

  const chartConfig = {
    headcount: {
      label: "Headcount",
      color: "hsl(var(--primary))",
    },
    occupancy: {
      label: "Occupancy (%)",
      color: "hsl(var(--muted-foreground))",
    }
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Workforce Trends</CardTitle>
        <CardDescription>Headcount and occupancy rates over the past week</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Screen Reader Table */}
        <table className="sr-only">
          <caption>Workforce Trends Data</caption>
          <thead>
            <tr>
              <th>Date</th>
              <th>Headcount</th>
              <th>Occupancy (%)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.date}>
                <td>{row.date}</td>
                <td>{row.headcount}</td>
                <td>{row.occupancy}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Visual Chart */}
        <div className="h-[300px] w-full mt-4" aria-hidden="true">
          <ChartContainer config={chartConfig} className="h-full w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorHeadcount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--color-headcount)" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="var(--color-headcount)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} opacity={0.3} />
                <XAxis 
                  dataKey="date" 
                  axisLine={false} 
                  tickLine={false} 
                  tickMargin={10} 
                  fontSize={12} 
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Area 
                  type="monotone" 
                  dataKey="headcount" 
                  stroke="var(--color-headcount)" 
                  fillOpacity={1} 
                  fill="url(#colorHeadcount)" 
                  strokeWidth={2} 
                />
              </AreaChart>
            </ResponsiveContainer>
          </ChartContainer>
        </div>
      </CardContent>
    </Card>
  );
}
