import React from 'react';
import PropTypes from 'prop-types';

const Message = ({ text, sender }) => {
  return (
    <div className={`message ${sender}`}>
      {text.split('\n').map((line, i) => (
        <p key={i}>{line}</p>
      ))}
    </div>
  );
};

Message.propTypes = {
  text: PropTypes.string.isRequired,
  sender: PropTypes.oneOf(['user', 'bot']).isRequired
};

export default Message;