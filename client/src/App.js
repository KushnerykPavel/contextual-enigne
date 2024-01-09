import './App.css';
import React, {useEffect, useState} from 'react';
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import TextField from '@mui/material/TextField';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import DoneIcon from '@mui/icons-material/Done';
import ErrorIcon from '@mui/icons-material/Error';
import PendingIcon from '@mui/icons-material/Pending';
import JsonView from '@uiw/react-json-view';
import {lightTheme} from '@uiw/react-json-view/light';
import Divider from '@mui/material/Divider';


function ListComponent(props) {
    const [open, setOpen] = React.useState(false);

    const handleClick = () => {
        setOpen(!open);
    };

    return (<>
        <ListItemButton onClick={handleClick}>
            {props.body.ready ? props.body.isError ? <ErrorIcon color={'error'} /> : <DoneIcon color={'success'} /> : <PendingIcon/>}
            <ListItemText primary={props.body.url} sx={{ color: props.body.ready ? props.body.isError ? '#d32f2f' : '#2e7d32' : '' }}/>
            {open ? <ExpandLess/> : <ExpandMore/>}
        </ListItemButton>
        <Collapse in={open} timeout="auto" unmountOnExit>
            <JsonView value={props.body} style={lightTheme}/>
        </Collapse>
        <Divider />
    </>)
}


function App() {
    const [receivedData, setReceivedData] = useState({});
    useEffect(() => {
        const ws = new WebSocket(`${process.env.REACT_APP_WS_URL}/ws`);
        // Event handler when WebSocket is opened
        ws.onopen = () => {
            console.log('WebSocket connected');
        };

        ws.onerror = (event) => {
            console.error('WebSocket error:', event);
        };

        ws.onclose = function (event) {
            console.log(event.code)
        }

        // Event handler when receiving messages from WebSocket
        ws.onmessage = (event) => {
            try {
                let data = JSON.parse(event.data)
                if (data.url) {
                    let responseUrl = data.url;
                    data.ready = true

                    setReceivedData(prevState => {
                        // Object.assign would also work
                        return {...prevState, ...{[responseUrl]: data}};
                    })

                }

            } catch (e) {
                console.log(e)
            }

        };


    }, []);


    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Authorization", "Bearer demo");

        let url = data.get('url')
        const raw = JSON.stringify({
            "url": url
        });

        const requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch(`${process.env.REACT_APP_HTTP_URL}/api/extract`, requestOptions)
            .then(response => response.text())
            .then(result => {

                let responseBody = JSON.parse(result);
                let data = {ready: false, url: url}

                if(responseBody.error !== undefined) {
                    data.ready = true
                    data.error = responseBody.error
                    data.isError = true
                }
                setReceivedData(prevState => {
                    // Object.assign would also work
                    return {...prevState, ...{[url]: data}};
                })
            })
            .catch(error => console.log('error', error));

    };

    return (
        <Box>
            <CssBaseline/>
            <AppBar position="relative">
                <Toolbar>
                    <Typography variant="h6" color="inherit" noWrap>
                        Contextual engine
                    </Typography>
                </Toolbar>
            </AppBar>
            <main>
                {/* Hero unit */}
                <Box
                    sx={{
                        bgcolor: 'background.paper',
                        pt: 4,
                        pb: 6,
                    }}
                >
                    <Container maxWidth="md">
                        <Typography
                            component="h1"
                            variant="h2"
                            align="center"
                            color="text.primary"
                            gutterBottom
                        >
                            Contextual engine
                        </Typography>
                        <Typography variant="h5" color="text.secondary" paragraph >
                            Demo project for contextual targeting engine. The project has next features:<br/>
                            1. Detecting content language<br/>
                            2. Founding keywords of content<br/>
                            3. Detecting IAB category list<br/>
                            <br/>
                            <b>Project works in async matter, processing of one page takes more 1m</b>  <br/> <br/>

                            List of url processing states:<br/>
                            <PendingIcon/> - url currently processing <br/>
                            <DoneIcon color={'success'} /> - url processed successfully <br/>
                            <ErrorIcon color={'error'} />  - url processed with error <br/>
                        </Typography>
                        <Box component="form" onSubmit={handleSubmit} noValidate sx={{mt: 1}}>
                            <Stack
                                sx={{pt: 4}}
                                direction="row"
                                spacing={2}
                                justifyContent="center"
                            >
                                <TextField
                                    margin="normal"
                                    required
                                    fullWidth
                                    id="url"
                                    label="Page url"
                                    name="url"
                                    placeholder="https://example.com/test"

                                    autoFocus
                                />
                                <Button
                                    type="submit"
                                    fullWidth
                                    variant="contained"
                                    sx={{mt: 1, mb: 2, width: 1 / 2}}
                                >
                                    Extract
                                </Button>
                            </Stack>
                        </Box>
                        <List>
                            {
                                Object.keys(receivedData).map(el => <ListComponent key={el} body={receivedData[el]}/>)
                            }
                        </List>
                    </Container>
                </Box>
            </main>
            {/* Footer */}
            <Box sx={{bgcolor: 'background.paper', p: 6}} component="footer">
                <Typography variant="h6" align="center" gutterBottom>
                    Footer
                </Typography>
                <Typography
                    variant="subtitle1"
                    align="center"
                    color="text.secondary"
                    component="p"
                >
                    <Link color="inherit" href="https://adscrawl-hub.pp.ua/">
                        Powered by adscrawl-hub
                    </Link>
                </Typography>
            </Box>
            {/* End footer */}
        </Box>

    );
}


export default App;
