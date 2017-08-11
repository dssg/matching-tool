import {
  DiscreteColorLegend,
  HorizontalGridLines,
  makeWidthFlexible,
  VerticalBarSeries,
  XAxis,
  XYPlot,
  YAxis,
} from 'react-vis'
import React from 'react'
import d3 from 'd3'

const FlexibleXYPlot = makeWidthFlexible(XYPlot)

export default class DurationBarChart extends React.Component {
	constructor(props) {
		super(props)
	}

	render() {
		return (
			<div className="mdl-grid">
				<div>
					<DiscreteColorLegend
          	orientation="horizontal"
          	items={["1 day", "10 days", "90 days"]} />
        </div>
        <div>
					<FlexibleXYPlot
	          animation
	          margin={{ left: 100, right: 100 }}
	          xType="ordinal"
	          stackBy="y"
	          height={330}>
	          <HorizontalGridLines />
	          <YAxis />
	          <XAxis />
	          <VerticalBarSeries
	          	data={[
	          		{x: 'Jail', y: 50},
	          		{x: 'Jail & Homeless', y: 30},
	          		]}
	          	opacity={0.8} />
	          <VerticalBarSeries
	          	data={[
	          		{x: 'Jail', y: 20},
	          		{x: 'Jail & Homeless', y: 30},
	          		]}
	          	opacity={0.8} />
	          <VerticalBarSeries
	          	data={[
	          		{x: 'Jail', y: 30},
	          		{x: 'Jail & Homeless', y: 40},
	          		]}
	          	opacity={0.8} />
	        </FlexibleXYPlot>
	        </div>
			</div>
		)
	}
}