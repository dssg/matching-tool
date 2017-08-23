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
			<div>
				<div className="mdl-cell">
					<DiscreteColorLegend
          	orientation="horizontal"
          	items={["0 day", "1 day", "2-9 days", "10-89 days", "90+ days"]} />
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
	          {this.props.data.map((entry) => (
	          	<VerticalBarSeries
	          		data={entry}
	          		opacity={0.8} />
	          ))}
	        </FlexibleXYPlot>
	        </div>
			</div>
		)
	}
}
