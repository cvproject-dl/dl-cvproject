import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {Tab,Box,AppBar,Tabs,Typography} from '@material-ui/core';
import PropTypes from 'prop-types';
import Cars from './cars';
import Search from './search'
import { Gradient } from 'react-gradient';

const gradients = [
  ['#bd19d6', '#ea7d10'],
  ['#ff2121', '#25c668'],
];


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}



const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    width: '80%',
    margin:"0px auto"
  },
  tab:{
    fontWeight:"bold",
    fontSize:"1.2rem",
    margin:"10px auto"
  },
  container:{
    height: "100%",
    display: "flex",
   flexDirection:"column"
  }

}));

  const Nav = () => { 

  const classes = useStyles();
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div className={classes.container}>
      <Gradient
                gradients={ gradients } // required
                property="background"
                duration={ 3000 }
                angle="45deg"
                >
      <div className={classes.root}>
          <h1 style={{textAlign:"center",color:'white'}}>Car Model Identification</h1>
        <AppBar position="static" style={{backgroundColor:'white',borderRadius:'12px'}}>
          <Tabs
            TabIndicatorProps={{style: {background:'black'}}}
            value={value}
            onChange={handleChange}
            // indicatorColor={white}
            style={{color:"black"}}
            aria-label="scrollable force tabs example"
          >
            <Tab label="Cars"  className={classes.tab}  {...a11yProps(0)}/>
            <Tab label="Search" className={classes.tab}  {...a11yProps(1)}/>
          </Tabs>
        </AppBar>
      </div>
      <div>
        <TabPanel value={value} index={0}>
          <Cars/>
        </TabPanel>
        <TabPanel value={value} index={1}>
          <Search />
        </TabPanel>
      </div>
      </Gradient>
    </div>
  );
}

export default Nav;