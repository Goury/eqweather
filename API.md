# API endpoints documentation

## Preamble

API is read-only, accepting only `GET`, `HEAD` and `OPTIONS` requests.

No authentication is required, just query what you need.

### `GET` query parameter `format` sets the output format

`api` will return graphical HTML pages.

`json` will return raw unformatted JSON.

### `GET` query parameter `page` returns the given page

If not set, any query will return the first page.

It will also return links to the next and to the previous pages and the total number of objects in the query.

## Endpoints

### `/api/`

root endpoint, returns links for cell and timestamp list endpoints .

### `/api/grid_cell/`

API endpoint to view grid cells.\
These are all the cells in the database.\
Each contains cell coordinates and a link to query every weather forecast for the given cell.

supports `GET` query parameters to filter and order the query:

`ordering` can be `id` or `-id`, will sort the query by id, ascending or descending.

`id__gte` will query for cells with id greater or equal to the value .\
`id__lte` will query for cells with id less or equal to the value.\
`id` will query for cells with the exact id.\
`id__gt` will query for cells with id greater than the value.\
`id__lt` will query for cells with id less than the value.\
`grid_id` will query for cells with the exact grid id.

### `/api/times/`

API endpoint to view available weather forecast timestamps.\
These are all the timestamps for which there is any data.\
Each contains readable date and time and a link to query all the data points for the given time.

supports `GET` query parameters to order the query:

`ordering` can be `when` or `-when`, will sort the query by timestamp, ascending or descending.

### `/api/forecasts/<when>/`

API endpoint to view weather forecasts for a given period of time.\
Each forecast also contains a link to query forecasts for all the timestamps from the same cell.

supports `GET` query parameters to filter and order the query:

`ordering` can be `cell_id`, `-cell_id`, `temperature`, `-temperature`, `humidity`, `-humidity`, will sort the query by cell id, temperature or humidity, ascending or descending.

`temperature__gte` will query for forecasts where temperature is greater or equal to the value.\
`temperature__lte` will query for forecasts where temperature is less or equal to the value.\
`temperature` will query for forecasts where temperature is equal to the value.\
`temperature__gt` will query for forecasts where temperature is greater than the value.\
`temperature__lt` will query for forecasts where temperature is less than the value.\
`humidity__gte` will query for forecasts where humidity is greater or equal to the value.\
`humidity__lte` will query for forecasts where humidity is less or equal to the value.\
`humidity` will query for forecasts where humidity is equal to the value.\
`humidity__gt` will query for forecasts where humidity is greater than the value.\
`humidity__lt` will query for forecasts where humidity is less than the value.


### `/api/grid_cell/<id>`

This is a single grid cell.\
It contains cell coordinates and a link to query every weather forecast for it.

### `/api/grid_cell/<id>/forecasts/`

API endpoint to view weather forecasts for a given cell.\
Each forecast also contains a link to query all the cell forecasts for the same timestamp.

supports `GET` query parameters to filter and order the query:

`ordering` can be `when`, `-when`, `temperature`, `-temperature`, `humidity`, `-humidity`, will sort the query by tiimestamp, temperature or humidity, ascending or descending.

`temperature__gte` will query for forecasts where temperature is greater or equal to the value.\
`temperature__lte` will query for forecasts where temperature is less or equal to the value.\
`temperature` will query for forecasts where temperature is equal to the value.\
`temperature__gt` will query for forecasts where temperature is greater than the value.\
`temperature__lt` will query for forecasts where temperature is less than the value.\
`humidity__gte` will query for forecasts where humidity is greater or equal to the value.\
`humidity__lte` will query for forecasts where humidity is less or equal to the value.\
`humidity` will query for forecasts where humidity is equal to the value.\
`humidity__gt` will query for forecasts where humidity is greater than the value.\
`humidity__lt` will query for forecasts where humidity is less than the value.
