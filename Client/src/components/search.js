import React, {useState } from 'react'
import { makeStyles} from '@material-ui/core/styles';
import { DropzoneArea } from 'material-ui-dropzone';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import {Box, Button, Grid,Card,CardContent,CardMedia,Typography,FormControl,Select,MenuItem} from '@material-ui/core';
import LoadingOverlay from 'react-loading-overlay';
import BounceLoader from 'react-spinners/BounceLoader';



const useStyles = makeStyles({
  dropzone:{
    width:'60%',
    margin:'25px auto',

  },
  root: {
    width: 345,
    margin:'10px',
    height:'340px',
  }
});

function Search() {
  const classes = useStyles();
  
 
  const [loading, setLoading] = useState(false)
  const[fileInput,setFileInput]=useState([]) 
  const [result, setResult] = useState([])
  const [carstate,setcarstate]=useState('sfcars')
 

  const uploadImage = async e => {
    setLoading(true)
    const formData = new FormData();
    formData.append('image', fileInput);
    formData.append('model',carstate)
  
      const options = {
        method: 'POST',
        body: formData,
      };

      const res = await fetch(
        'http://127.0.0.1:5000/predict', options
      )
      const file =await res.json()
        
       setResult(file.predictions)
       console.log("new api")
       console.log(file.predictions)
       setLoading(false)
  }

  return (
    <Box component="div" style={{height:'1000vh'}}>
      
      <Grid className={classes.dropzone} container justify='center' alignItems='center'>
      <DropzoneArea
          style={{marginTop:'10px'}}
          acceptedFiles={['image/*']}
          dropzoneText={"Drag and drop an image here or click"}
          onChange={(file)=>{
          setFileInput(file[0])}}
      />

      <FormControl variant="outlined" style={{marginTop:'10px',width:'300px',border:'3px solid black',borderRadius:'12px'}}>
        
          <Select
            value={carstate}
            onChange={(event) => {setcarstate(event.target.value);}}
            >
          <MenuItem value='sfcars'>Sfcars</MenuItem>
          <MenuItem value='indcars'>Indcars</MenuItem>
          </Select>
      </FormControl>
      <Button
        variant="contained"
        color="basic" style={{marginTop:'10px',marginLeft:'10px',height:'50px',border:'3px solid black',borderRadius:'12px'}}
        startIcon={<CloudUploadIcon />}
        onClick={uploadImage}>
          Upload
      </Button>
      </Grid>

      {loading ? (
        <LoadingOverlay
            active={true}
            spinner={<BounceLoader />}
            text='Loading...'
        />
      ) : (

        <Grid container style={{margin:'10px auto'}}>  
        {result.map((it,idx) => (
          <React.Fragment>
          {it.map( (it1, idx1) => (
          <Grid item container xs={12} sm={4} justify="center" alignItems="center" key={idx1}>
          <Card className={classes.root} >
          <CardContent>
          <CardMedia component="img" alt="car image"
          image={it1.car_details.image} style={{borderRadius:"8px",height:'215px'}}/>
          </CardContent>
          <CardContent>
            <Typography gutterBottom variant="h6" component="h2">{it1.car_details.name}</Typography>
            <Typography gutterBottom variant="h6" component="h2">{(it1.confidence*100).toFixed(2)+"%"}</Typography>
          </CardContent>
          </Card>
          </Grid>
          
          ))}
          <hr style={{width:'90%'}}/>
          </React.Fragment>
        ))}
        </Grid>
      )}
     
    </Box>
  )
}

export default Search
