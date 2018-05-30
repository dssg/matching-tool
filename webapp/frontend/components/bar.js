import { DiscreteColorLegend } from 'react-vis'
import { HorizontalGridLines } from 'react-vis'
import { makeWidthFlexible } from 'react-vis'
import { VerticalBarSeries } from 'react-vis'
import { XAxis } from 'react-vis'
import { XYPlot } from 'react-vis'
import { YAxis } from 'react-vis'
import { Hint, Crosshair } from 'react-vis'
import React from 'react'

const FlexibleXYPlot = makeWidthFlexible(XYPlot)

const styles = {
  tooltips: {
    background: "#3a3a48",
    borderRadius: "4px",
    padding: "7px 7px",
    fontSize: "12px",
    textAlign: "left",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.5)",
    color: "white",
    whiteSpace: "nowrap"
  }
}

export default class DurationBarChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: false
    }
  }

  handleOnValueMouseOver = (v) => {
    this.setState({value: v})
  }

  handleOnSeriesMouseOut = (v) => {
    this.setState({value: false})
  }

  renderHint() {
    if (this.state.value) {
      return (
        <Hint value={this.state.value}>
          <div style={styles.tooltips}>
            <p>{ (typeof this.state.value.y0 != 'undefined') ? (this.state.value.y - this.state.value.y0).toFixed(2) : (this.state.value.y).toFixed(2)}%</p>
          </div>
        </Hint>
      )
    }
  }

  render() {
    if (this.props.data == null) {
      return (
        <div className="container">
          <h3>No data!</h3>
        </div>
      )
    } else {
      return (
        <div>
          <div className="col-sm-4">
            <FlexibleXYPlot
              animation
              margin={{ left: 100, right: 5, top: 20 }}
              xType="ordinal"
              stackBy="y"
              width={300}
              height={270}>
              <HorizontalGridLines />
              <YAxis
                tickFormat={v => `${v}%`}
                style={{
                  ticks: {fontSize: 14}
                }} />
              <YAxis
                hideLine
                hideTicks
                left={-80}
                title={'Percent of Population'}
                style={{
                  title: {fontSize: 14, color: '#000000'}
                }}
                top={85} />
              <XAxis
                style={{
                  ticks: {fontSize: 14}
                }}
              />
              {this.props.data[0].map((entry, idx) => (
                <VerticalBarSeries
                  data={entry}
                  key={idx}
                  animation={false}
                  onValueMouseOver={this.handleOnValueMouseOver}
                  onValueMouseOut={this.handleOnSeriesMouseOut}
                  opacity={0.8}>
                </VerticalBarSeries>
              ))}
              {this.renderHint()}
            </FlexibleXYPlot>
          </div>
          <div className="col-sm-2">
            <DiscreteColorLegend
              margin={{ left: 1, right: 1 }}
              orientation="vertical"
              items={this.props.data[1]} />
          </div>
        </div>
      )
    }
  }
}
