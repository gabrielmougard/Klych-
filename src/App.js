import '@material/react-button/dist/button.css';
import Button from '@material/react-button';
import React, { Component } from 'react';
import Camera from 'react-html5-camera-photo';
import 'react-html5-camera-photo/build/css/index.css';
import Gallery from 'react-grid-gallery';


import dataUri_to_image from './utils.js';
import loading_img from './loading.gif';
import './App.css';


// For the demo version should change this for final deployment
// behind a reverse proxy
const addr = 'https://home.plawn-inc.science/face';
const upload_adress = 'api/find';
const photo_address = 'https://cdn.plawn-inc.science/face/';
const final_upload_adress = addr + '/' + upload_adress;

// Settings 
const title = 'Klych--';

// same as on the flask python app || Shouldn't be changed
const filename = 'file';

const prepare_photo_links = (links, adrr) => links.map(link => prepare_link(adrr + link));
const prepare_link = link => ({ src: link, thumbnail: link, thumbnailWidth: NaN, thumbnailHeight: NaN });

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      camera_on: true,
      photo_roll_on: false,
      is_loading: false,
      photos: [],
      bt_class: 'center__'
    }
    this.set_loading = () => this.setState({ is_loading: true });
    this.loading_done = () => this.setState({ is_loading: false });

    this.upload_photo = async dataUri => {
      const fd = new FormData();
      fd.append(filename, dataUri_to_image(dataUri));
      this.setState({ camera_on: false });
      this.set_loading();
      const res = await fetch(final_upload_adress, { method: 'POST', body: fd }); // be careful here => change the adress as needed
      const t = await res.json();
      const photos = prepare_photo_links(t.found.map(i => i.split('/').slice(-1)), photo_address);
      this.setState({ bt_class: photos.length > 0 ? 'just_padded' : 'center__' });
      this.setState({
        photos: photos//here to | was tested on a remote site
      });
      this.loading_done();
      this.setState({ photo_roll_on: true });
    }

  }


  render() {
    document.title = title;
    return (
      <div>
        <div className="App">
          <h1>Find your pictures</h1>
          {this.state.is_loading &&
            <img src={loading_img} style={{ maxWidth: '100%' }} className="center__"></img>}
          {this.state.photo_roll_on &&
            <Button className={this.state.bt_class} onClick={() => this.setState({ camera_on: true, photo_roll_on: false })}>Try again</Button>
          }
          {this.state.camera_on &&
            <Camera
              onTakePhoto={this.upload_photo}
            />}
          <div>
            {this.state.photo_roll_on &&
              <Gallery
                images={this.state.photos}
                onSelectImage={i => { this.state.photos[i].isSelected = !this.state.photos[i].isSelected; }}
              />}
          </div>
        </div>
      </div>
    );
  }
}

export default App;
