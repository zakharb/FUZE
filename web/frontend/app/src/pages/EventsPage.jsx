import { forwardRef, useRef, useEffect, useState, useMemo } from 'react';
import { Fragment } from 'react';
import { useTable, useRowSelect } from 'react-table';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Badge from '@mui/material/Badge';
import AddIcon from '@mui/icons-material/Add';
import UploadIcon from '@mui/icons-material/Upload';
import DownloadIcon from '@mui/icons-material/Download';
import FunctionsIcon from '@mui/icons-material/Functions';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import CopyAllIcon from '@mui/icons-material/CopyAll';
import './Table.css';
import Container from '@mui/material/Container';
import ReportIcon from '@mui/icons-material/Report';
import Chip from '@mui/material/Chip';
import DrawerFilter from "../components/DrawerFilter"
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import PlaybookViewer from "../components/Playbook"
import Modal from '@mui/material/Modal';

import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { Page, Text, View, Document, StyleSheet } from '@react-pdf/renderer';

import {
  fetchEventsData,
  } from "../api/ApiDataPage"


const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 1000,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
  maxHeight: '800px', 
  overflowY: 'auto',
};

const styles = StyleSheet.create({
  page: {
    flexDirection: 'row',
    backgroundColor: '#E4E4E4'
  },
  section: {
    margin: 10,
    padding: 10,
    flexGrow: 1
  }
});


function Table() {
  // consts
  const [rawData, setRawData] = useState([]);
  const [data, setData] = useState([]);
  const [dataCount, setDataCount] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [checked, setChecked] = useState(true);
  const [playbook, setPlaybook] = useState('');
  // Date time now and -1 week
  const now = new Date();
  const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  const [startDate, setStartDate] = useState(oneWeekAgo.toISOString().slice(0, 16));
  const [endDate, setEndDate] = useState(now.toISOString().slice(0, 16));

  const columns = useMemo(
    () => [
      {
        Header: 'Severity',
        accessor: 'severity',
        Cell: ({ value }) => {
          let color;
          switch (value) {
            case 'high':
              color = 'error';
              break;
            case 'med':
              color = 'warning';
              break;
            default:
              color = 'secondary';
              break;
          }
          return (
            <Chip 
              label={value} 
              color={color} />
          );
        },
        minWidth: 50,
      },      
      {
        Header: 'Name',
        accessor: 'name',
      },
      {
        Header: 'Description',
        accessor: 'description',
        Cell: ({ value }) => <div style={{ width: '500px' }}>{value}</div>,
      },
      {
        Header: 'Classification',
        accessor: 'tactic',
      },
    ],
    []
  );
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    selectedFlatRows,
    state: { selectedRowIds },
  } = useTable(
    {
      columns,
      data,
    },
    useRowSelect
  )
  const [isDeleteButtonVisible, setIsDeleteButtonVisible] = useState(false);
  const [editingRow, setEditingRow] = useState(null);
  const initFormData = {
    name: '',
    description: '',
    tactic: '',
    src_ip: '',
    dst_ip: '',
    events: '',
  }
  const [formData, setFormData] = useState(initFormData);

  //infinite scrolling
  const [visibleRows, setVisibleRows] = useState(30);

  const navigate = useNavigate();

  // use effects
  useEffect(() => {
    fetchEventsData(setData, setRawData)
    const filteredResults = rawData.filter(item =>
      item.positive == true
    );
    setData(filteredResults);
  }, []);

  useEffect(() => {
    if (Object.keys(selectedRowIds).length > 0) {
      setIsDeleteButtonVisible(true);
    } else {
      setIsDeleteButtonVisible(false);
    }
  }, [selectedRowIds]);

  useEffect(() => {
    setDataCount(data.length);
  }, [data]);

  // handlers
  const handleDownload = () => {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'incidents.json';
    link.click();
  };

  const handleSearch = (event) => {
    const { value } = event.target;
    setSearchTerm(value);
    const filteredResults = rawData.filter(item =>
      item.name.toLowerCase().includes(value.toLowerCase()) ||
      item.description.toLowerCase().includes(value.toLowerCase()) ||
      item.tactic.toLowerCase().includes(value.toLowerCase()) ||
      item.time.includes(value)
    );
    setData(filteredResults);
  };

  const handleFalsePositives = (event) => {
    setChecked(event.target.checked);
    var positiveResults;
    if (!checked) {
      positiveResults = rawData.filter(item =>
        item.positive == true
      );
    } else {
      positiveResults = rawData
    }
    setData(positiveResults);
  };

  const handleEditClick = async (row) => {
    try {
      const editData = await fetchEventsRuleGet(row.original.id);
      setFormData({
        name: editData.name,
        description: editData.description,
        tactic: editData.tactic,
        severity: editData.severity,
        positive: editData.positive,
        events: editData.events,
      });
    } catch (error) {
      console.error(error);
    }
    setEditingRow(row);
  };

  // Filters
  const [filters, setFilters] = useState({
    'Severity': '',
    'Name': '',
    'Tactic': '',
  });

  const handleApplyFilters = () => {
    fetchEventsFilter(filters, startDate, endDate, setData, setRawData);
  };

  const handleScroll = (e) => {
    const { scrollTop, clientHeight, scrollHeight } = e.currentTarget;
    if (scrollTop + clientHeight === scrollHeight) {
      setVisibleRows((prevVisibleRows) => prevVisibleRows + 10);
    }
  };

  return (
    <Container sx={{ minWidth: '1000px'}} maxWidth="xl"
      style={{ height: '1200px', overflow: 'auto'
      }}
      onScroll={handleScroll} 
    >
      <div className="table">
        <Grid container sx={{padding: 3}} >
          <Grid item xl={6}>
            <Stack spacing={2} direction="row">
              <Button variant="outlined" color="secondary" startIcon={<DownloadIcon />} onClick={handleDownload}>
                Save
              </Button>
              {/* <FormGroup>
                <FormControlLabel 
                  control={<Switch  checked={checked} onChange={handleFalsePositives}/>} 
                  label="NVIDIA AI" 
                  />
              </FormGroup>               */}
            </Stack>        
          </Grid>
          <Grid item xl={6}>
            <Grid container justifyContent="flex-end" alignItems="center">
              <TextField
                id="standard-basic"
                label="Search"
                variant="standard"
                value={searchTerm}
                onChange={handleSearch}
              />
              <Badge badgeContent={dataCount} color="primary">
                <FunctionsIcon color="action" />
              </Badge>            
              <DrawerFilter 
                filters={filters} 
                setFilters={setFilters} 
                applyFilters={handleApplyFilters} 
                startDate={startDate} 
                setStartDate={setStartDate} 
                endDate={endDate}
                setEndDate={setEndDate} 
              />
            </Grid>
          </Grid>
        </Grid>              
        <table {...getTableProps()}>
          <thead>
            {headerGroups.map(headerGroup => (
              <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
              ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.slice(0, visibleRows).map((row, i) => {
              prepareRow(row);
              return (
                <Fragment key={row.id}>
                  <tr onClick={() => handleEditClick(row)} {...row.getRowProps()}>
                    {row.cells.map(cell => {
                      return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>;
                    })}
                  </tr>
                  {editingRow === row ? (
                    <tr key={`${row.id}-edit`}>
                      <td colSpan={columns.length + 2}>
                        <EditForm formData={formData} setFormData={setFormData} row={row} data={formData} onClose={() => setEditingRow(null)} />
                      </td>
                    </tr>
                  ) : null}
                </Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </Container>
)
}

function EditForm({ formData, setFormData, row, data, onClose }) {
  const [additionalField, setAdditionalField] = useState('');
  const [newEvent, setNewEvent] = useState('');  
  const navigate = useNavigate();

  const handleChange = (field) => (event) => {
    setFormData((prevState) => ({
      ...prevState,
      [field]: event.target.value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const editData = await fetchEventsRuleEdit(row.original.id, formData);
    } catch (error) {
      console.error(error);
    }
    onClose();
  };

  const handleCancelClick = () => {
    onClose();
  };

  const handleAddEvent = () => {
    const newEventData = { [newEvent]: 1 };
    setNewEvent('');
    setFormData((prevState) => ({
      ...prevState,
      meta_events: [...prevState.meta_events, newEventData],
    }));
  };

  const handleEventChange = (index, field) => (event) => {
    const newEvents = [...formData.meta_events];
    newEvents[index][field] = event.target.value;
    setFormData(prevState => ({
      ...prevState,
    }));
  };

  const handleNewEventChange = (event) => {
    setNewEvent(event.target.value);
  };

const handleDeleteEvent = (index) => () => {
  const newEvents = [...formData.meta_events];
  newEvents.splice(index, 1);
  setFormData((prevState) => ({
    ...prevState,
    meta_events: newEvents,
  }));
};
const formattedData = JSON.stringify(data.events, null, 2);

const handleApplyFilters = () => {
  fetchEventsFilter(filters, startDate, endDate, setData, setRawData);
};

let controller;

const cancelStreaming = () => {
  if (controller) {
    controller.abort();
    setModalText('Streaming aborted.');
  }
};

const handlePlaybookClick = async (event) => {
  handleOpen();
  cancelStreaming();
  controller = new AbortController();
  console.log(controller.aborted);
  setModalText('Generating, please wait...');


  try {
    const response = await fetchEventsPlaybook(row.original.id, controller);
    const reader = response.body.getReader();
    let result = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      if (controller.signal.aborted) {
        setModalText('Streaming aborted.');
        break;
      }

      result += new TextDecoder().decode(value);
      setModalText(result);
    }
  } catch (error) {
    console.error('Error fetching streaming data:', error);
  }
};


const PdfDocument = () => (
  <Document>
    <Page size="A4">
      <View>
        <Text>Hello, this is a PDF document created using React and @react-pdf/renderer!</Text>
      </View>
    </Page>
  </Document>
);

const handleDownload = () => {
  const pdfBlob = PdfDocument();
  const blobUrl = URL.createObjectURL(pdfBlob);
  const link = document.createElement('a');
  link.href = blobUrl;
  link.download = 'iot365-playbook.pdf';
  link.click();
  URL.revokeObjectURL(blobUrl);
};

  const [open, setOpen] = useState(false);
  const [modalText, setModalText] = useState('');
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

return (
  <div className="edit-form">
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <Typography id="modal-modal-title" variant="h6" component="h2" sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          Report
          <Button variant="outlined" color="secondary" startIcon={<DownloadIcon />} onClick={handleDownload}>
            Save
          </Button>
          <Button variant="outlined" color="secondary" startIcon={<DownloadIcon />} onClick={cancelStreaming}>
            Cancel
          </Button>
        </Typography>
        <div
          id="modal-modal-description"
          sx={{ mt: 2, maxHeight: '400px', overflowY: 'auto' }}
          dangerouslySetInnerHTML={{ __html: modalText }}
        />
      </Box>
    </Modal>  
    <form onSubmit={handleSubmit}>
      <Grid container spacing={2} direction="row" sx={{paddingLeft: 15, paddingRight: 2}}>
        <Grid item xl={8}>
          <Button sx={{marginRight: 2}} size="small" variant="outlined" color="error" onClick={handleCancelClick}>
            Close
          </Button>
          <Button sx={{marginRight: 2}} size="small" variant="outlined" color="primary" onClick={handlePlaybookClick}>
            Report
          </Button>
        </Grid>
        {/* <Grid item>
          {data.positive ? (
            <Chip label="Positive" color="error" variant="outlined"/>
          ) : (
            <Chip label="False Positive" color="secondary" variant="outlined"/>
          )}
        </Grid> */}
      </Grid>
      <Grid id="edit_data" container spacing={2} sx={{paddingTop: 5, paddingLeft: 15, paddingBottom: 10, paddingRight: 2}}>
        <Grid item xl={8}>
          <TextField
            value={data.name}
            id="standard-basic" 
            fullWidth
            label="Name" 
            onChange={handleChange('name')}
            variant="standard"
          />
        </Grid>
        <Grid item xl={3}>
          <TextField
            value={data.severity}
            id="standard-basic" 
            fullWidth
            label="Severity" 
            onChange={handleChange('severity')}
            variant="standard"
          />
        </Grid>
        <Grid item xl={8}>
          <TextField
            value={data.description}
            id="standard-basic" 
            fullWidth
            label="Description" 
            onChange={handleChange('description')}
            variant="standard"
          />
        </Grid>
        <Grid item xl={3}>
          <TextField
            value={data.tactic}
            id="standard-basic" 
            fullWidth
            label="Classification" 
            onChange={handleChange('tactic')}
            variant="standard"
          />
        </Grid>
        <Grid item xl={12}>
        </Grid>
        {/* {
          Object.entries(data.rules).map(([key, event]) => (
            <Grid container spacing={2} sx={{paddingTop: 5, paddingLeft: 2, paddingBottom: 2}}>
              <Grid item xl={12}>
                <Link 
                  to={`/events?${new URLSearchParams({'node_name': event}).toString()}`}>
                  <Button 
                    size="small" 
                    variant="outlined" 
                    color="primary"
                  >
                    {event.tax}
                  </Button>
                </Link>          
              </Grid>
              <Grid item xl={4} sx={{paddingTop: 2}}>
                <TextField
                  value={event.node_tap}
                  fullWidth
                  label="Tap"
                  variant="standard"
                />                
              </Grid>
              <Grid item xl={4}>
                <TextField
                  value={event.node_name}
                  fullWidth
                  label="Source"
                  variant="standard"
                />                
              </Grid>
              <Grid item xl={3}>
                <TextField
                  value={new Date(event.time +'Z').toLocaleString()}
                  fullWidth
                  label="Date"
                  variant="standard"
                />                
              </Grid>
              <Grid item xl={11}>
                <TextField
                  value={event.name}
                  fullWidth
                  label="Name" 
                  variant="standard"
                />                
              </Grid>
              <Grid item xl={12}>
                {Object.keys(event.fields).map(key => (
                  <TextField
                    key={key}
                    value={event.fields[key]}
                    label={key}
                    variant="standard"
                  />
                ))}
              </Grid>
            </Grid>
          ))
        } */}
      </Grid>
    </form>
  </div>
);
}

export default Table;
