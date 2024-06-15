import { useState } from 'react';
import { useTheme } from '@mui/material/styles';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Input } from '@mui/material';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

function getStyles(name, normName, theme) {
  return {
    fontWeight:
      normName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

export default function MultipleSelect({onChange, normName, name, optionValues}) {
  const theme = useTheme();
  const [value, setValue] = useState(normName ? normName : []);

  const handleChange = (event) => {
    console.log(onChange);
    const {
      target: { value },
    } = event;
    setValue(
      typeof value === 'string' ? value.split(',') : value,
    );
    onChange;
  };

  return (
    <div>
      <FormControl fullWidth>
        <Select
          labelId="demo-multiple-name-label"
          id="demo-multiple-name"
          multiple
          value={value}
          input={<Input label={name} />}
          onChange={handleChange}
          MenuProps={MenuProps}
        >
          {optionValues.map((name) => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, value, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
}