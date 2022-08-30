import Button from 'react-bootstrap/Button';
const Header = () => {
    return (
   
            <div className='header'>
                <div className='text-header text-light'> Compare Crypto </div>
                <Button variant="outline-light" type="submit" className=''>
                          Get Started
                </Button>
            </div>
      
    )
}

export default Header