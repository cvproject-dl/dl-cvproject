import React,{useState,useEffect} from "react";
import {Grid,Box,Card,CardContent,CardMedia,Typography,FormControl,Select,InputAdornment,TextField,MenuItem,InputLabel} from '@material-ui/core'
import { makeStyles} from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import SearchIcon from '@material-ui/icons/Search';
import InfiniteScroll from 'react-infinite-scroll-component';

const useStyles = makeStyles({
    loader:{
        position:'absolute',
        top:'50%',
        left:'50%'
    },
    root: {
        maxWidth: 345,
        margin:'10px',
        height:'340px'
      },
      select:{
          margin:'20px auto',
      }
    
});

function Cars() {
    const classes = useStyles();


    const [page, setPageNo]=useState(1);
    const [loading,setLoading] = useState(false);
    const [cardata,setcars] = useState([]);
    const [carstate,setcarstate] = useState('sfcars')
    const [search,setsearch] = useState('');
    const [invalid, setInvalid]=useState(false);
    
    
        const searchFunc = async() => {
            console.log("called")
            const data=await fetch ("http://127.0.0.1:5000/cars?model="+carstate+"&search="+search+"&page="+page);
            const jdata=await data.json();
            setInvalid( jdata.invalidPage);
            setcars( [...cardata, ...jdata.cars]);
            setLoading(true);
        }
        useEffect(()=>{
            searchFunc();
        },[carstate, search, page])

    
        if(loading === false)
        {
            return(
                <div>
                <div className={classes.loader}>
                    <CircularProgress size="5rem" style={{color:"black"}}/>
                </div>
                </div>   
            );
            
        }
        else{

        return(
            <Box component="div">    
                <Grid container justify='center' alignItems='center' className={classes.select}>
                <TextField 
                style={{width:'50%'}}
                id="outlined-basic" 
                variant="outlined"
                label="Search Cars"
                onChange={ (e) => {
                    setcars([]);
                    setsearch(e.target.value)
                    setPageNo(1)
                   }}
                    InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <SearchIcon fontSize="large"/>
                          </InputAdornment>
                        )
                      }} />
                    <FormControl variant="outlined" style={{marginLeft:'10px'}}>
                        <InputLabel id="demo-simple-select-outlined-label">Model</InputLabel>
                        <Select
                        value={carstate}
                        onChange={(event) => {
                            setcars([])
                            setcarstate(event.target.value);
                            setPageNo(1)
                        }}
                        label="Model"
                        >
                        <MenuItem value='sfcars'>Sfcars</MenuItem>
                        <MenuItem value='indcars'>Indcars</MenuItem>
                        </Select>
                    </FormControl> 
                </Grid>
                
                
                

                <InfiniteScroll
                    dataLength={cardata.length} 
                    next={() => {
                        console.log("next");
                        setPageNo(page+1)}}
                    hasMore={!invalid}
                    endMessage={
                        <p style={{ textAlign: 'center' }}>
                            <h2>Yay! You have seen it all</h2>
                        </p>
                    }
                    scrollThreshold={0.8}
                >
                    
                <Grid container style={{margin:"10px auto"}}>
                    {console.log(cardata)}
                {cardata.map((it,idx)=>(
                    <Grid item container xs={12} sm={6} md={4} justify="center" alignItems="center" key={idx}>
                        <Card className={classes.root} >
                        <CardContent>
                        <CardMedia component="img" alt="car image"
                        image={it.image} style={{borderRadius:"8px",height:'230px',width:'310px'}}/>
                        </CardContent>
                        <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                            {it.name}
                        </Typography>
                        </CardContent>
                        </Card>
                    </Grid>
                ))}
                </Grid>


            </InfiniteScroll>

            </Box>
            
            );
        }
}

export default Cars;
