import React from "react";

const SuggestionsList = props => {
  const {
    suggestions,
    inputValue,
    onSelectSuggestion,
    displaySuggestions,
    selectedSuggestion
  } = props;

  if (inputValue && displaySuggestions) {
    if (suggestions.length > 0) {
      return (
        <ul className="suggestions-list">
          {suggestions.map((suggestion, index) => {
            const isSelected = selectedSuggestion === index;
            const classname = `suggestion ${isSelected ? "selected" : ""}`;
            return (
              <li
                key={index}
                className={classname}
                onClick={() => onSelectSuggestion(index)}
              >
                {suggestion}
              </li>
            );
          })}
        </ul>
      );
    } else {
      return <div>No suggestions available...</div>;
    }
  }
  return <></>;
};
const Autocomplete = () => {
  const [inputValue, setInputValue] = React.useState("");
  const [filteredSuggestions, setFilteredSuggestions] = React.useState([]);
  const [selectedSuggestion, setSelectedSuggestion] = React.useState(0);
  const [displaySuggestions, setDisplaySuggestions] = React.useState(false);
  

  const suggestions = [
    "Oathbringer",
    "American Gods",
    "A Game of Thrones",
    "Prince of Thorns",
    "Assassin's Apprentice",
    "The Hero of Ages",
    "The Gunslinger"
  ];

  const onChange = event => {
    const value = event.target.value;
    setInputValue(value);

    const filteredSuggestions = suggestions.filter(suggestion =>
      suggestion.toLowerCase().includes(value.toLowerCase())
    );

    setFilteredSuggestions(filteredSuggestions);
    setDisplaySuggestions(true);
  };

  const onSelectSuggestion = index => {
    setSelectedSuggestion(index);
    setInputValue(filteredSuggestions[index]);
    setFilteredSuggestions([]);
    setDisplaySuggestions(false);
  };

  return (
    <>
      <h1>React Autocomplete</h1>
      <input
        className="user-input"
        type="text"
        onChange={onChange}
        value={inputValue}
      />
      <SuggestionsList
        inputValue={inputValue}
        selectedSuggestion={selectedSuggestion}
        onSelectSuggestion={onSelectSuggestion}
        displaySuggestions={displaySuggestions}
        suggestions={filteredSuggestions}
      />
    </>
  );
};


export default Autocomplete