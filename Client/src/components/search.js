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
    maxWidth: 345,
    margin:'10px',
    height:'340px'
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
       
       console.log(result);
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
          <Grid item container xs={12} sm={3} justify="center" alignItems="center" key={idx}>
          <Card className={classes.root} >
          <CardContent>
          <CardMedia component="img" alt="car image"
          image={it.image} style={{borderRadius:"8px",width:'310px',height:'230px'}}/>
          </CardContent>
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">{it.name}</Typography>
          </CardContent>
          </Card>
          </Grid>
        ))}
        </Grid>
      )}
     
    </Box>
  )
}

export default Search
