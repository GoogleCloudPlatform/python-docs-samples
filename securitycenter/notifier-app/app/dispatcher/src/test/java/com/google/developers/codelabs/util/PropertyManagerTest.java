package com.google.developers.codelabs.util;


import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

/**
 * The Class PropertyManagerTest.
 */
@RunWith(MockitoJUnitRunner.class)
@SuppressWarnings("javadoc")
public class PropertyManagerTest {

  @Mock
  private PropertyReader reader;

  private PropertyManager manager;

  @Before
  public void setup() {
    manager = new PropertyManager(reader);
  }

  @Test(expected = IllegalStateException.class)
  public void withAEmptyEnvironmentVariableThrowsIllegalException() {
    String propertyName = "PROPERTY";
    when(reader.getProperty(propertyName)).thenReturn("");
    manager.getRequiredProperty(propertyName);
  }

  @Test(expected = IllegalStateException.class)
  public void withANullEnvironmentVariableThrowsIllegalException() {
    String propertyName = "PROPERTY";
    when(reader.getProperty(propertyName)).thenReturn(null);
    manager.getRequiredProperty(propertyName);
  }

  @Test
  public void returnsEnvironmentVariableValue() {
    String propertyName = "PROPERTY";
    String expected = "VALUE";
    when(reader.getProperty(propertyName)).thenReturn(expected);
    String value = manager.getRequiredProperty(propertyName);
    assertEquals(expected, value);
  }

  @Test
  public void getEnvironmentVariableReturnsEmptyEnvironmentVariableValue() {
    String propertyName = "PROPERTY";
    String expected = "";
    when(reader.getProperty(propertyName)).thenReturn(expected);
    String value = manager.getProperty(propertyName);
    assertEquals(expected, value);
  }

}
