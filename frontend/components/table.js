import React from 'react'
import Reactable from 'reactable'

export default class TableList extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <Reactable.Table
        className="table"
        sortable
        pageButtonLimit={5}
        itemsPerPage={15}
        data={this.props.data} />
    )
  }
}
