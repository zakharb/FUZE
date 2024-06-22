import { forwardRef, useRef, useEffect, useState, useMemo } from 'react';
import { Fragment } from 'react';
import { useTable, useRowSelect } from 'react-table';
import Container from '@mui/material/Container';
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
import MultipleSelect from '../components/MultipleSelect.jsx';

import {
  fetchData,
  fetchTaxanomyGet,
  fetchTaxanomyAdd,
  fetchTaxanomyDel,
  fetchTaxanomyEdit,
  } from "../api/ApiTaxanomyPage.jsx"

function Table() {
  const [rawData, setRawData] = useState([]);
  const [data, setData] = useState([]);
  const [dataCount, setDataCount] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [NormRules, setNormRules] = useState([]);
  const [name, setName] = useState('');
  const [editingRow, setEditingRow] = useState(null);
  const initFormData = {}
  const [formData, setFormData] = useState(initFormData);
  const columns = useMemo(
    () => [
      {
        Header: 'Main',
        accessor: 'tax_main',
      },
      {
        Header: 'Object',
        accessor: 'tax_object',
      },
      {
        Header: 'Action',
        accessor: 'tax_action',
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

  useEffect(() => {
    fetchData(setData, setRawData)
  }, []);

  useEffect(() => {
    setDataCount(data.length);
  }, [data]);

  useEffect(() => {
    if (Object.keys(selectedRowIds).length > 0) {
      setIsDeleteButtonVisible(true);
    } else {
      setIsDeleteButtonVisible(false);
    }
  }, [selectedRowIds]);

  const handleDownload = () => {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'rules.json';
    link.click();
  };

  const handleFileSelect = (event) => {
    const formData = new FormData();
    formData.append("file", event.target.files[0]);
    Import(setData, formData)
  };

  const handleSearch = (event) => {
    const { value } = event.target;
    setSearchTerm(value);
    const filteredResults = rawData.filter(item =>
      item.name.toLowerCase().includes(value.toLowerCase()) ||
      item.severity.toLowerCase().includes(value.toLowerCase())
    );
    setData(filteredResults);
  };

  const handleAddClick = async () => {
    const data = {
      "tax_main": "New_tax",
      "tax_action": "",
      "tax_object": "",
    };
    try {
      const addData = await fetchTaxanomyAdd(data);
      setData((oldRows) => [...oldRows, addData]);
    } catch (error) {
      console.error(error);
    }
  };
  
  const handleDeleteAll = async () => {
    try {
      const data = await fetchDeleteAll();
      setData((oldRows) => [...oldRows, data]);
    } catch (error) {
      console.error(error);
    }
  };

  const handleEditClick = async (row) => {
    try {
      const editData = await fetchTaxanomyGet(row.original.id);
      setFormData({
        name: editData.name,
        severity: editData.severity,
      });
    } catch (error) {
      console.error(error);
    }
    setEditingRow(row);
  };

  const handleDelClick = async (row) => {
    try {
      const deleteData = await fetchTaxanomyDel(row.original.id);
    } catch (error) {
      console.error(error);
    }
    setData(data.filter((oldRow) => oldRow.id !== row.original.id));
  };

  const handleCopyClick = async (row) => {
    try {
      const copyData = await fetchTaxanomyCopy(row.original.id);
      setData((oldRows) => [...oldRows, copyData]);
      fetchData(setData, setRawData)
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container sx={{ minWidth: '1000px'}} maxWidth="xl">
      <div className="table">
        <Grid container sx={{padding: 3}} >
          <Grid item xl={6}>
            <Stack spacing={2} direction="row">
              <Button variant="contained" color="warning" startIcon={<AddIcon />} onClick={handleAddClick}>
                Add
              </Button>
              <Button variant="outlined" color="error" startIcon={<DeleteIcon />} onClick={handleDeleteAll}>
                Clear
              </Button>
              <Button variant="outlined" color="secondary" startIcon={<DownloadIcon />} onClick={handleDownload}>
                Export
              </Button>
              <Button variant="outlined" color="secondary" startIcon={<UploadIcon />} component="label">
                Import
                <input
                  type="file"
                  accept=".json"
                  hidden
                  onChange={handleFileSelect} 
                />
              </Button>              
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
            </Grid>
          </Grid>
        </Grid>              
        <table {...getTableProps()}>
          <thead>
            {headerGroups.map(headerGroup => (
              <tr {...headerGroup.getHeaderGroupProps()}>
              <th style={{ width: '120px' }}></th>
                {headerGroup.headers.map(column => (
                  <th {...column.getHeaderProps()}>{column.render('Header')}</th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row, i) => {
              prepareRow(row);
              return (
                <Fragment key={row.id}>
                  <tr onClick={() => handleEditClick(row)} {...row.getRowProps()}>
                    <td>
                      <IconButton 
                        className="actionButtons"
                        color="error" 
                        size="small"
                        onClick={() => handleDelClick(row)}>
                        <DeleteIcon fontSize="inherit" />
                      </IconButton>
                      <IconButton 
                        className="actionButtons"
                        color="secondary" 
                        size="small"
                        onClick={() => handleCopyClick(row)}>
                        <CopyAllIcon fontSize="inherit" />
                      </IconButton>
                      <IconButton 
                        className="actionButtons"
                        color="primary" 
                        size="small"
                        onClick={() => handleEditClick(row)}>
                        <EditIcon fontSize="inherit" />
                      </IconButton>
                    </td>
                    {row.cells.map(cell => {
                      return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>;
                    })}
                  </tr>
                  {editingRow === row ? (
                    <tr key={`${row.id}-edit`}>
                      <td colSpan={columns.length + 2}>
                        <EditForm NormRules={NormRules} formData={formData} setFormData={setFormData} row={row} data={formData} onClose={() => setEditingRow(null)} />
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

function EditForm({ NormRules, formData, setFormData, row, data, onClose }) {
  const [additionalField, setAdditionalField] = useState('');
  const [newNode, setNewNode] = useState('');  
  const handleChange = (field) => (event) => {
    setFormData((prevState) => ({
      ...prevState,
      [field]: event.target.value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const editData = await fetchTaxanomyEdit(row.original.id, formData);
    } catch (error) {
      console.error(error);
    }
    onClose();
  };

  const handleCancelClick = () => {
    onClose();
  };

  const handleAddNode = () => {
    const newNodeData = { [newNode]: 1 };
    setNewNode('');
    setFormData((prevState) => ({
      ...prevState,
      nodes: [...prevState.nodes, newNodeData],
    }));
  };

  const handleNodeChange = (index, field) => (event) => {
    const newNodes = [...formData.nodes];
    newNodes[index][field] = event.target.value;
    setFormData(prevState => ({
      ...prevState,
    }));
  };

  const handleNewNodeChange = (event) => {
    setNewNode(event.target.value);
  };

  const handleDeleteNode = (index) => () => {
    const newNodes = [...formData.nodes];
    newNodes.splice(index, 1);
    setFormData((prevState) => ({
      ...prevState,
      nodes: newNodes,
    }));
  };

return (
  <div className="edit-form">
    <form onSubmit={handleSubmit}>
      <Grid container spacing={2} direction="row" sx={{paddingLeft: 15}}>
        <Grid item>
        <Button size="small" variant="outlined" color="error" onClick={handleCancelClick}>
          Cancel
        </Button>
        </Grid>
        <Grid item>
        <Button size="small" variant="contained" color="primary" type="submit">
          Save
        </Button>
        </Grid>
      </Grid>
      <Grid container spacing={2} sx={{paddingTop: 5}}>
        <Grid item xs={0} xl={1}>
        </Grid>
        <Grid item xs={3} xl={3}>
          <TextField
            value={data.tax_main}
            id="standard-basic" 
            fullWidth
            label="Tax Main" 
            onChange={handleChange('tax_main')}
            variant="standard"
          />
        </Grid>
        <Grid item xs={3} xl={3}>
          <TextField
            value={data.tax_object}
            id="standard-basic"
            fullWidth
            label="Object" 
            onChange={handleChange('tax_object')}
            variant="standard"
          />
        </Grid>
        <Grid item xs={3} xl={3}>
          <TextField
            value={data.tax_action}
            id="standard-basic"
            fullWidth
            label="Action" 
            onChange={handleChange('tax_action')}
            variant="standard"
          />
        </Grid>
      </Grid>
    </form>
  </div>
);
}

export default Table;
